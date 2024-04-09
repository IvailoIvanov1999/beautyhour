from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from beautifyme.products.models import Product, Category, ProductCart, Order

User = get_user_model()


class MyCartViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

        self.category1 = Category.objects.create(name='Category 1', slug='category-1', status=True)
        self.category2 = Category.objects.create(name='Category 2', slug='category-2', status=False)

        self.product1 = Product.objects.create(name='Product 1', price=10, quantity=5, description='Description 1',
                                               product_image='mediafiles/media/products/Accessories/accessory.jpeg',
                                               category=self.category1,
                                               product_added_user_id=self.user.id)
        self.product2 = Product.objects.create(name='Product 2', price=15, quantity=3, description='Description 2',
                                               product_image='mediafiles/media/products/Accessories/accessory.jpeg',
                                               category=self.category2, product_added_user_id=self.user.id)

        self.cart_item1 = ProductCart.objects.create(user=self.user, product=self.product1, quantity=2)
        self.cart_item2 = ProductCart.objects.create(user=self.user, product=self.product2, quantity=1)

        self.order1 = Order.objects.create(user=self.user, total_price=25, quantity=3,
                                           product_names='Product 1, Product 2')
        self.order2 = Order.objects.create(user=self.user, total_price=30, quantity=4,
                                           product_names='Product 1, Product 2')

    def test_my_cart_view(self):
        self.client.login(email='testuser@example.com', password='testpassword')

        response = self.client.get(reverse('my-cart', kwargs={'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['cart_products']), 2)

        self.assertEqual(response.context['total_price'], 35)
        self.assertEqual(response.context['total_count'], 3)

    def test_order_proceed_view_redirect(self):
        self.client.login(email='testuser@example.com', password='testpassword')

        self.client.post(reverse('add-to-cart', args=[self.product1.id]))
        self.client.post(reverse('add-to-cart', args=[self.product2.id]))

        initial_cart_items_count = ProductCart.objects.filter(user=self.user).count()

        self.assertEqual(initial_cart_items_count, 2)

        response = self.client.post(reverse('submit-order'))

        self.assertRedirects(response, reverse('thanks-purchase'))

        self.assertEqual(ProductCart.objects.filter(user=self.user).count(), 0)

    def test_anonymous_user_cant_add_in_cart(self):
        response = self.client.post(reverse('add-to-cart', args=[self.product1.id]))

        self.assertEqual(response.status_code, 302)

        self.assertURLEqual(
            response.url,
            f'/account/login/?next={reverse("add-to-cart", args=[self.product1.id])}'
        )

    def test_all_orders_page_requires_superuser_or_staff_access(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('all-orders'))

        self.assertEqual(response.status_code, 403)

    def test_all_orders_page_accessible_to_superuser(self):
        superuser = User.objects.create_superuser(email='admin@example.com', password='adminpassword')

        self.client.login(email='admin@example.com', password='adminpassword')

        response = self.client.get(reverse('all-orders'))

        self.assertEqual(response.status_code, 200)

    def test_all_orders_page_accessible_to_staff_user(self):
        self.user.is_staff = True
        self.user.save()

        self.client.login(email='testuser@example.com', password='testpassword')

        response = self.client.get(reverse('all-orders'))

        self.assertEqual(response.status_code, 200)

    def test_thanks_purchase_view_only_authenticated_users(self):
        self.client.login(email='testuser@example.com', password='testpassword')

        response = self.client.get(reverse('thanks-purchase'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'web/thanks-for-purchase.html')
