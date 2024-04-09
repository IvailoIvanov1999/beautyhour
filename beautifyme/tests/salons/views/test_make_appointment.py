from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import date

from beautifyme.accounts.models import Profile
from beautifyme.salons.models import Appointment, Salon

User = get_user_model()


class MakeAppointmentViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.salon = Salon.objects.create(
            name='Test Salon',
            description='Test description',
            city='Sofia',
            phone_number='123456789',
            email_address='test@example.com',
            address='Test address',
            logo='mediafiles/media/salons/Alice/alice-salon-jpeg',
            user=self.user
        )
        try:
            self.profile = Profile.objects.get(user_id=self.user)
        except Profile.DoesNotExist:
            # Create a test profile
            self.profile = Profile.objects.create(
                user_id=self.user,
                first_name='testname',
                last_name='testlastname',
                address='testaddress',
            )

    def test_make_appointment_unauthenticated_user(self):
        # Make a POST request to the make_appointment view without logging in
        response = self.client.post(reverse('make-appointment'))

        # Check if the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/salon/make-appointment/')

    def test_user_has_applied_appointment(self):

        self.appointment1 = Appointment.objects.create(
            profile_id=self.profile.user_id,
            salon_id=self.salon.id,
            date='2024-05-09',

        )

        # Check if the appointment was successfully made
        self.assertEqual(Appointment.objects.count(), 1)
