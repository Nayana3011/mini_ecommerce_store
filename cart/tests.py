from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User

from cart.cart import Cart
from catalogue.models import Category, Product, ProductVariant


class CartTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='seller',
            password='test123'
        )

        self.category = Category.objects.create(
            name='Mobile'
        )

        self.product = Product.objects.create(
            name='Samsung M30',
            description='Test Product',
            category=self.category,
            seller=self.user
        )

        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='SAM001',
            size='128GB',
            colour='Black',
            price=10000,
            stock_quantity=10
        )

    def get_request(self):

        request = self.factory.get('/')

        middleware = SessionMiddleware(
            lambda req: None
        )

        middleware.process_request(request)

        request.session.save()

        return request

    def test_add_to_cart(self):

        request = self.get_request()

        cart = Cart(request)

        cart.add(self.variant, qty=2)

        self.assertEqual(len(cart), 2)

    def test_remove_from_cart(self):

        request = self.get_request()

        cart = Cart(request)

        cart.add(self.variant, qty=2)

        cart.remove(self.variant)

        self.assertEqual(len(cart), 0)

    def test_update_quantity(self):

        request = self.get_request()

        cart = Cart(request)

        cart.add(self.variant, qty=1)

        cart.update_qty(self.variant, 5)

        self.assertEqual(len(cart), 5)

    def test_clear_cart(self):

        request = self.get_request()

        cart = Cart(request)

        cart.add(self.variant, qty=3)

        cart.clear()

        self.assertEqual(len(cart), 0)