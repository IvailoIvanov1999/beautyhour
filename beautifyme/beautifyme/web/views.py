from django.shortcuts import render
from django.views import generic as views

from beautifyme.products.models import Product


class HomePageView(views.ListView):
    template_name = 'web/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(quantity__gt=0)
