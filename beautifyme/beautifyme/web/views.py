from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins as auth_mixins
from django.db.models import Sum, F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic as views
from django.urls import reverse

from beautifyme.core.view_mixins import OwnerRequiredMixin, \
    IsSuperuserOrIsStaffPermissionsRequiredMixin
from beautifyme.products.models import Product, Category, ProductCart, Order

from django.db import IntegrityError


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        try:
            if request.user.is_authenticated:
                cart_item = ProductCart.objects.get(user=request.user, product=product)

                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

                product.quantity += 1
                product.save()

                return redirect(reverse('my-cart', kwargs={'user_id': request.user.id}))
            else:
                return HttpResponse("User not authenticated.")
        except ProductCart.DoesNotExist:
            return HttpResponse("Product not found in cart.")

    return HttpResponse("Invalid request.")


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    try:
        if product.quantity > 0:
            product.quantity -= 1
            product.save()

            cart, created = ProductCart.objects.get_or_create(user=request.user, product=product)

            if not created:
                cart.quantity += 1
                cart.save()

        referring_url = request.META.get('HTTP_REFERER')
        return redirect(referring_url or 'index')

    except IntegrityError:
        return HttpResponse("An error occurred while trying to add the product to the cart.")


class HomePageView(views.ListView):
    template_name = 'web/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(quantity__gt=0)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status=True)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CategoryProductsView(views.ListView):
    model = Product
    template_name = 'web/category-products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        queryset = queryset.filter(category=category)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['category'] = Category.objects.get(slug=slug)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class MyCartView(OwnerRequiredMixin, views.ListView):
    template_name = 'web/my-cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        queryset = ProductCart.objects.filter(user=self.request.user)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(product__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        total_price = ProductCart.objects.filter(user_id=user_id).aggregate(
            total_price=Sum(F('product__price') * F('quantity')))
        total_count = ProductCart.objects.filter(user_id=user_id).aggregate(total_count=Sum('quantity'))

        context['total_price'] = total_price['total_price'] if total_price['total_price'] is not None else 0
        context['total_count'] = total_count['total_count'] if total_count['total_count'] is not None else 0

        return context


@login_required
def order_proceed_view(request):
    if request.method == 'POST':
        user = request.user

        if user.id:
            cart_products = ProductCart.objects.filter(user_id=user.id)

            total_price = cart_products.aggregate(total_price=Sum(F('product__price') * F('quantity')))['total_price']

            total_quantity = cart_products.aggregate(total_quantity=Sum('quantity'))['total_quantity']

            order = Order.objects.create(user=user, total_price=total_price, quantity=total_quantity)

            product_names = ', '.join([product_in_cart.product.name for product_in_cart in cart_products])
            order.product_names = product_names
            order.save()

            user_cart_products = user.productcart_set.all()
            user_cart_products.delete()

            return redirect('thanks-purchase')

        return HttpResponse('Invalid request')


class AllOrdersView(IsSuperuserOrIsStaffPermissionsRequiredMixin, views.ListView):
    template_name = 'web/all-orders-for-staff-only.html'
    context_object_name = 'orders'
    queryset = Order.objects.all().order_by('-id')


class ThanksPurchaseView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = 'web/thanks-for-purchase.html'
