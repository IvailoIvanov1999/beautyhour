from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from beautifyme.core.view_mixins import OwnerRequiredMixin, AdminPermissionsRequiredMixin
from beautifyme.salons.forms import SalonCreateForm, SalonEditForm
from beautifyme.salons.models import Salon, Appointment


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
        return Salon.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salons_with_index = [(i, salon) for i, salon in enumerate(context['salons'])]
        context['salons_with_index'] = salons_with_index
        return context


class SalonDetailsView(views.DetailView):
    template_name = 'salons/salon-details.html'

    def get_queryset(self):
        queryset = Salon.objects.filter(pk=self.kwargs['pk'])
        queryset = queryset.prefetch_related('appointment_set')
        return queryset

class SalonEditView(AdminPermissionsRequiredMixin, OwnerRequiredMixin, views.UpdateView):
    form_class = SalonEditForm
    template_name = 'salons/salon-edit.html'

    def get_queryset(self):
        return Salon.objects.filter(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse("salon-details", kwargs={
            "pk": self.object.pk,
        })


class SalonDeleteView(AdminPermissionsRequiredMixin, OwnerRequiredMixin, views.DeleteView):
    model = Salon
    template_name = 'salons/salon-delete.html'
    success_url = reverse_lazy('user-salons')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class SalonCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = SalonCreateForm
    template_name = "salons/salon-create.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def make_appointment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date = request.POST.get('appointment_date')
            salon_id = request.POST.get('salon_id')
            profile_id = request.POST.get('profile_id')

            Appointment.objects.create(
                date=date,
                salon_id=salon_id,
                profile_id=profile_id
            )

            return render(request, 'web/appointment-for-salon-applied.html')
