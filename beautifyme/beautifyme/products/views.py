from django.urls import reverse_lazy
from django.views import generic as views

from beautifyme.products.forms import AddProductForm
from beautifyme.products.models import Product


class AddProduct(views.CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'products/add-products.html'
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.product_added_user_id = self.request.user.id
        return super().form_valid(form)


class ProductDetailsView(views.DetailView):
    template_name = 'products/product-detail.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        if pk:
            return Product.objects.filter(pk=pk)
        else:
            return Product.objects.none()
