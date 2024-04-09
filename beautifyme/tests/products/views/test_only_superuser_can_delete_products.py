from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory

from beautifyme.products.models import Product, Category
from beautifyme.products.views import ProductEditView

User = get_user_model()


class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_user(email='admin@admin.com', password='admin',
                                                  is_superuser=True)
        self.staff_user = User.objects.create_user(email='staff@staff.com', password='staff',
                                                   is_staff=True)
        self.normal_user = User.objects.create_user(email='user@user.com', password='user')

        self.category = Category.objects.create(
            name='Test Category',
            category_image='mediafile/category.png',
            slug='test-category',
            status=True
        )

        self.product = Product.objects.create(name='Test Product', description='Test Description', price=100,
                                              quantity=1,
                                              product_image='mediafiles/test.jpg',
                                              category=self.category,
                                              product_added_user_id=1,
                                              )

    def test_super_user_can_delete(self):
        url = reverse('delete-product', kwargs={'pk': self.product.pk})
        request = self.factory.get(url)
        request.user = self.superuser
        response = ProductEditView.as_view()(request, pk=self.product.pk)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_cannot_delete(self):
        url = reverse('delete-product', kwargs={'pk': self.product.pk})
        request = self.factory.get(url)
        request.user = self.normal_user

        with self.assertRaises(PermissionDenied):
            ProductEditView.as_view()(request, pk=self.product.pk)

    def test_normal_user_cannot_delete(self):
        url = reverse('delete-product', kwargs={'pk': self.product.pk})
        request = self.factory.get(url)
        request.user = self.normal_user

        with self.assertRaises(PermissionDenied):
            ProductEditView.as_view()(request, pk=self.product.pk)
