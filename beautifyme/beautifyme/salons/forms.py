from django import forms

from beautifyme.salons.models import Salon


class SalonCreateForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = (
            'name',
            'description',
            'city',
            'logo',
            'phone_number',
            'email_address',
            'address',
        )


class SalonEditForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = (
            'name',
            'description',
            'city',
            'logo',
            'phone_number',
            'email_address',
            'address',
        )
