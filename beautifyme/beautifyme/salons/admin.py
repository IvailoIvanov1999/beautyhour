from django.contrib import admin

from beautifyme.salons.models import Salon, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',  'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'city', 'phone_number',)
    list_filter = ('name', 'description', 'city',)
