import os

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from beautifyme.accounts.models import Profile


def salon_image_upload_path(instance, filename):
    basefilename, extension = os.path.splitext(filename)

    return f'media/salons/{instance.name}/{basefilename}{extension}'


UserModel = get_user_model()


class Salon(models.Model):
    CITY_CHOICES = [
        ('Sofia', 'Sofia'),
        ('Plovdiv', 'Plovdiv'),
        ('Varna', 'Varna'),
        ('Burgas', 'Burgas'),
        ('Ruse', 'Ruse'),
        ('Stara Zagora', 'Stara Zagora'),
        ('Pleven', 'Pleven'),
        ('Sliven', 'Sliven'),
        ('Dobrich', 'Dobrich'),
        ('Shumen', 'Shumen'),
        ('Pernik', 'Pernik'),
        ('Yambol', 'Yambol'),
        ('Haskovo', 'Haskovo'),
        ('Blagoevgrad', 'Blagoevgrad'),
        ('Veliko Tarnovo', 'Veliko Tarnovo'),
        ('Gabrovo', 'Gabrovo'),
        ('Vratsa', 'Vratsa'),
        ('Kyustendil', 'Kyustendil'),
        ('Pazardzhik', 'Pazardzhik'),
    ]

    name = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(max_length=300, blank=False, null=False)
    city = models.CharField(choices=CITY_CHOICES, max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=30, blank=False, null=False)
    email_address = models.EmailField(blank=False, null=False)
    address = models.CharField(max_length=150, blank=False, null=False)
    logo = models.ImageField(upload_to=salon_image_upload_path, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='owned_salons')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Appointment for {self.profile.full_name} at {self.salon.name} on {self.date}"
