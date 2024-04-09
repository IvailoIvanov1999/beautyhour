from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic as views
from django.urls import reverse

from beautifyme.core.view_mixins import AdminPermissionsRequiredMixin, OwnerRequiredMixin, \
    IsStaffPermissionsRequiredMixin, IsSuperuserOrIsStaffPermissionsRequiredMixin
from beautifyme.products.models import Product, Category, ProductCart, Order

from django.db import IntegrityError


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
        return Product.objects.filter(quantity__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status=True)
        return context


class CategoryProductsView(views.ListView):
    model = Product
    template_name = 'web/category-products.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['category'] = Category.objects.get(slug=slug)
        return context


class MyCartView(OwnerRequiredMixin, views.ListView):
    template_name = 'web/my-cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        user_id = self.request.user.id
        return ProductCart.objects.filter(user_id=user_id)

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


class ThanksPurchaseView(views.TemplateView):
    template_name = 'web/thanks-for-purchase.html'
