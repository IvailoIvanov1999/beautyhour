from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import generic as views
from django.urls import reverse
from beautifyme.products.models import Product, Category, ProductCart

from django.db import IntegrityError


def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        try:
            if request.user.is_authenticated:
                cart_item = ProductCart.objects.get(user=request.user, product=product)
                cart_item.delete()

                product.quantity += 1
                product.save()

                return redirect(reverse('my-cart', kwargs={'user_id': request.user.id}))
            else:
                return HttpResponse("User not authenticated.")
        except ProductCart.DoesNotExist:
            return HttpResponse("Product not found in cart.")

    return HttpResponse("Invalid request.")


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
        return Product.objects.all()

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


class MyCartView(views.ListView):
    template_name = 'web/my-cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return ProductCart.objects.filter(user_id=user_id)
        else:
            return ProductCart.objects.none()
