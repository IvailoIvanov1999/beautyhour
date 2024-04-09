from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from beautifyme.salons.models import Salon
from beautifyme.salons.views import SalonEditView

User = get_user_model()


class SalonEditViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner_user = User.objects.create_user(email='owner@email.com', password='testpassword')
        self.non_owner_user = User.objects.create_user(email='non_owner@email.com', password='testpassword')
        # self.salon = Salon.objects.create(name='Test Salon', user=self.owner_user)

        self.salon = Salon.objects.create(
            name='Test Salon',
            description='This is a dummy salon description.',
            city='Sofia',
            phone_number='1234567890',
            email_address='dummy@example.com',
            address='123 Dummy St.',
            logo='mediafiles/media/salons/Beauty/logo_1.jpg',
            user=self.owner_user
        )

    def test_salon_edit_by_owner(self):
        url = reverse('salon-edit', kwargs={'pk': self.salon.pk})
        data = {
            'name': 'Updated Salon Name',
            'description': 'TEST',
            'city': 'Sofia',
            'phone_number': '12345',
            'email_address': 'dummy@example.com',
            'address': '123 Dummy St.',
            'logo': 'mediafiles/media/salons/Beauty/logo_1.jpg',
            'user': self.owner_user
        }
        request = self.factory.post(url, data)
        request.user = self.owner_user

        view = SalonEditView.as_view()
        response = view(request, pk=self.salon.pk)

        self.assertIsInstance(response, HttpResponseRedirect)

        # Follow the redirect to get the final response
        final_response = self.client.get(response.url)

        # Ensure the final response is successful
        self.assertEqual(final_response.status_code, 200)

        # Check if the final response is the expected one
        self.assertTemplateUsed(final_response, 'salons/salon-details.html')

        # Check if the salon instance was updated in the database
        updated_salon = Salon.objects.get(pk=self.salon.pk)
        self.assertEqual(updated_salon.name, 'Updated Salon Name')
        self.assertEqual(updated_salon.description, 'TEST')
        self.assertEqual(updated_salon.city, 'Sofia')
        self.assertEqual(updated_salon.phone_number, '12345')
        self.assertEqual(updated_salon.email_address, 'dummy@example.com')
        self.assertEqual(updated_salon.address, '123 Dummy St.')
        self.assertEqual(updated_salon.logo, 'mediafiles/media/salons/Beauty/logo_1.jpg')
        self.assertEqual(updated_salon.user, self.owner_user)

    def test_salon_edit_by_non_owner(self):
        # Simulate a POST request to edit the salon by a non-owner
        url = reverse('salon-edit', kwargs={'pk': self.salon.pk})
        data = {'name': 'Updated Salon Name'}
        request = self.factory.post(url, data)
        request.user = self.non_owner_user

        # Instantiate the view and call its post method
        view = SalonEditView.as_view()

        # Expecting PermissionDenied exception
        with self.assertRaises(PermissionDenied):
            response = view(request, pk=self.salon.pk)

        # Check that the salon details remain unchanged
        self.salon.refresh_from_db()
        self.assertEqual(self.salon.name, 'Test Salon')
