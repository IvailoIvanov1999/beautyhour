from django.urls import path

from beautifyme.web.views import HomePageView, CategoryProductsView, add_to_cart, MyCartView, remove_from_cart

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('categories/<str:slug>/', CategoryProductsView.as_view(), name='category'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('my-cart/<int:user_id>/', MyCartView.as_view(), name='my-cart'),
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
]
