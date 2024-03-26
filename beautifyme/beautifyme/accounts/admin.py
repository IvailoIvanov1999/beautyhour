from django.contrib import admin

from beautifyme.accounts.models import Profile, BeautyHourUser


@admin.register(BeautyHourUser)
class BeautyHourUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_staff')
    search_fields = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',)
    search_fields = ('user__email', 'first_name', 'last_name',)
    readonly_fields = ('email',)
    list_filter = ('user__email', 'first_name', 'last_name',)

    def email(self, obj):
        return obj.user.email

    email.admin_order_field = 'user__email'
    email.short_description = 'Email'
