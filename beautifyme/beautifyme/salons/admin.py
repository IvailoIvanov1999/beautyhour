from django.contrib import admin

from beautifyme.salons.models import Salon, Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'date')
    list_filter = ('date',)
    search_fields = ('profile',)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'city', 'phone_number',)
    list_filter = ('name', 'description', 'city',)
