import os

from django.db import models


def product_image_upload_path(instance, filename):
    basefilename, extension = os.path.splitext(filename)

    return f'media/products/{instance.name}/{basefilename}{extension}'


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    category_image = models.ImageField(upload_to=product_image_upload_path, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    product_image = models.ImageField(upload_to=product_image_upload_path, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1, null=False, blank=False)
    description = models.CharField(max_length=3000, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
