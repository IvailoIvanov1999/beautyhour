from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from beautifyme.core.view_mixins import AdminPermissionsRequiredMixin, IsStaffPermissionsRequiredMixin, \
    IsSuperuserOrIsStaffPermissionsRequiredMixin
from beautifyme.products.forms import AddProductForm, EditProductForm
from beautifyme.products.models import Product


class AddProduct(IsSuperuserOrIsStaffPermissionsRequiredMixin, views.CreateView):
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


class ProductEditView(IsSuperuserOrIsStaffPermissionsRequiredMixin, views.UpdateView):
    form_class = EditProductForm
    template_name = 'products/edit-product.html'

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse("details-product", kwargs={
            "pk": self.object.pk,
        })


class ProductDeleteView(AdminPermissionsRequiredMixin, views.DeleteView):
    model = Product
    template_name = 'products/delete-product.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
