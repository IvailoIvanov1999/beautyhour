from django import forms

from beautifyme.products.models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'product_image', 'quantity', 'category']
