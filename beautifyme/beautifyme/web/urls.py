from django.urls import path

from beautifyme.web.views import HomePageView, CategoryProductsView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('categories/<str:slug>/', CategoryProductsView.as_view(), name='category')

]
