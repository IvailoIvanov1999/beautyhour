from django.shortcuts import render
from django.views import generic as views

from beautifyme.products.models import Product, Category


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
