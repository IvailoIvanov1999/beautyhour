from django.urls import path

from beautifyme.products.views import AddProduct, ProductDetailsView

urlpatterns = [
    path('add/', AddProduct.as_view(), name='add-product'),
    path('details/<int:pk>', ProductDetailsView.as_view(), name='details-product')
]
