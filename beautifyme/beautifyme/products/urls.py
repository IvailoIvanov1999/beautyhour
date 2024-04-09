from django.urls import path

from beautifyme.products.views import AddProduct, ProductDetailsView, ProductEditView, ProductDeleteView

urlpatterns = [
    path('add/', AddProduct.as_view(), name='add-product'),
    path('details/<int:pk>', ProductDetailsView.as_view(), name='details-product'),
    path('edit/<int:pk>', ProductEditView.as_view(), name='edit-product'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete-product')
]
