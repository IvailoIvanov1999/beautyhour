from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from beautifyme.core.view_mixins import OwnerRequiredMixin
from beautifyme.salons.forms import SalonCreateForm
from beautifyme.salons.models import Salon


class AllSalonsView(views.ListView):
    template_name = 'salons/all-salons.html'
    model = Salon
    context_object_name = 'salons'

    def get_queryset(self):
        return Salon.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salons_with_index = [(i, salon) for i, salon in enumerate(context['salons'])]
        context['salons_with_index'] = salons_with_index
        return context


class SalonsDetailsView(views.ListView):
    template_name = 'salons/user-salons.html'
    model = Salon
    context_object_name = 'salons'

    def get_queryset(self):
        return Salon.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salons_with_index = [(i, salon) for i, salon in enumerate(context['salons'])]
        context['salons_with_index'] = salons_with_index
        return context


class SalonDetailsView(views.DetailView):
    template_name = 'salons/salon-details.html'

    def get_queryset(self):
        return Salon.objects.filter(pk=self.kwargs['pk'])


class SalonEditView(OwnerRequiredMixin, views.UpdateView):
    pass


class SalonDeleteView(OwnerRequiredMixin, views.DeleteView):
    pass


class SalonCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = SalonCreateForm
    template_name = "salons/salon-create.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
