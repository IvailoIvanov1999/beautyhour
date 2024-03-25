from django.urls import path, include

from beautifyme.accounts.views import ProfileDetailsView, ProfileDeleteView, ProfileUpdateView, SignInUserView, \
    RegisterUserView, logout_user

urlpatterns = [
    path('login/', SignInUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path("signout/", logout_user, name="logout"),
    path('<int:pk>/', include([
        path('details/', ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', ProfileUpdateView.as_view(), name='profile-edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    ]))
]
