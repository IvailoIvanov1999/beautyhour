from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from beautifyme.salons.models import Salon
from beautifyme.salons.views import SalonDeleteView

User = get_user_model()


class SalonDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner_user = User.objects.create_user(email='owner@email.com', password='testpassword')
        self.non_owner_user = User.objects.create_user(email='non_owner@email.com', password='testpassword')
        self.salon = Salon.objects.create(name='Test Salon', user=self.owner_user)

    def test_salon_deletion_by_owner(self):
        url = reverse('salon-delete', kwargs={'pk': self.salon.pk})
        request = self.factory.post(url)
        request.user = self.owner_user

        view = SalonDeleteView.as_view()
        view(request, pk=self.salon.pk)

        self.assertFalse(Salon.objects.filter(pk=self.salon.pk).exists())

    def test_salon_deletion_by_non_owner(self):
        url = reverse('salon-delete', kwargs={'pk': self.salon.pk})
        request = self.factory.post(url)
        request.user = self.non_owner_user

        view = SalonDeleteView.as_view()

        with self.assertRaises(PermissionDenied):
            view(request, pk=self.salon.pk)

        self.assertTrue(Salon.objects.filter(pk=self.salon.pk).exists())
