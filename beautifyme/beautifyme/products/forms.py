from django import forms

from beautifyme.products.models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'product_image', 'quantity', 'category']


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'product_image', 'quantity', 'category']


class ProductSearchFrom(forms.Form):
    search_query = forms.CharField(max_length=150, required=False, label='Search')
