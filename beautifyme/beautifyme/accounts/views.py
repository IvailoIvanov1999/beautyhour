from django.forms import SelectDateWidget
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import views as auth_views, login, logout, get_user
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from beautifyme.accounts.forms import BeautyHourUserCreationForm
from beautifyme.accounts.models import BeautyHourUser, Profile
from beautifyme.core.view_mixins import OwnerRequiredMixin
from beautifyme.salons.models import Appointment


class SignInUserView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class RegisterUserView(views.CreateView):
    template_name = "accounts/register.html"
    form_class = BeautyHourUserCreationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


def logout_user(request):
    logout(request)
    return redirect('index')


class ProfileDetailsView(OwnerRequiredMixin, views.DetailView):
    template_name = "accounts/account-details.html"

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        appointments = profile.appointment_set.all()
        context['appointments'] = appointments.order_by('-date')
        return context


class ProfileUpdateView(OwnerRequiredMixin, views.UpdateView):
    template_name = "accounts/account-edit.html"
    fields = ("first_name", "last_name", "address", "profile_picture", "date_of_birth")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("profile-details", kwargs={
            "pk": self.object.pk,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["date_of_birth"].widget = SelectDateWidget(years=range(1900, datetime.now().year + 1))

        return form


class ProfileDeleteView(OwnerRequiredMixin, views.DeleteView):
    model = Profile
    template_name = "accounts/account-delete.html"
    success_url = reverse_lazy('register')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        success_url = self.get_success_url()
        self.object.delete()
        user.delete()
        return HttpResponseRedirect(success_url)
