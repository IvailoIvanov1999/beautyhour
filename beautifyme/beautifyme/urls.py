from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('beautifyme.web.urls')),
                  path('account/', include('beautifyme.accounts.urls')),
                  path('salon/', include('beautifyme.salons.urls')),
                  path('product/', include('beautifyme.products.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
