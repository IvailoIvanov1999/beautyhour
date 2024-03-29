from django.urls import path, include

from beautifyme.salons.views import SalonCreateView, SalonDetailsView, SalonEditView, SalonDeleteView, \
    SalonsDetailsView, AllSalonsView

urlpatterns = [
    path('create/', SalonCreateView.as_view(), name='salon-create'),
    path('all-salons', AllSalonsView.as_view(), name='all-salons'),
    path('user-salons/', SalonsDetailsView.as_view(), name='user-salons'),
    path('<int:pk>/', include([
        path('details/', SalonDetailsView.as_view(), name='salon-details'),
        path('edit/', SalonEditView.as_view(), name='salon-edit'),
        path('delete/', SalonDeleteView.as_view(), name='salon-delete')
    ]))
]
