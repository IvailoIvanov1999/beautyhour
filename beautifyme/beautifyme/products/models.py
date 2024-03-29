import os

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

User = get_user_model()


def product_image_upload_path(instance, filename):
    basefilename, extension = os.path.splitext(filename)

    return f'media/products/{instance.name}/{basefilename}{extension}'


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    category_image = models.ImageField(upload_to=product_image_upload_path, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    product_image = models.ImageField(upload_to=product_image_upload_path, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1, null=False, blank=False, validators=[MinValueValidator(1)])
    description = models.CharField(max_length=3000, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_added_user_id = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
