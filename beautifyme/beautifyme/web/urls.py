from django.urls import path

from beautifyme.web.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
]
