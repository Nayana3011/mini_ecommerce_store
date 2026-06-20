from django.test import TestCase, Client
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta

from catalogue.models import (
    Category,
    Product,
    ProductVariant
)

from orders.models import (
    Order,
    OrderItem
)


class CheckoutTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            username='buyer',
            password='test123'
        )

        self.seller = User.objects.create_user(
            username='seller',
            password='test123'
        )

        self.category = Category.objects.create(
            name='Mobile'
        )

        self.product = Product.objects.create(
            name='Samsung M30',
            description='Test',
            category=self.category,
            seller=self.seller
        )

        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='SAM001',
            size='128GB',
            colour='Black',
            price=10000,
            stock_quantity=10
        )

    def test_order_creation(self):

        self.client.login(
            username='buyer',
            password='test123'
        )

        session = self.client.session

        session['cart'] = {
            str(self.variant.id): 2
        }

        session.save()

        response = self.client.post(
            '/orders/checkout/',
            {
                'address': 'Calicut'
            }
        )

        self.assertEqual(
            Order.objects.count(),
            1
        )

    def test_stock_decrement(self):

        self.client.login(
            username='buyer',
            password='test123'
        )

        session = self.client.session

        session['cart'] = {
            str(self.variant.id): 2
        }

        session.save()

        self.client.post(
            '/orders/checkout/',
            {
                'address': 'Calicut'
            }
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock_quantity,
            8
        )

    def test_order_item_created(self):

        self.client.login(
            username='buyer',
            password='test123'
        )

        session = self.client.session

        session['cart'] = {
            str(self.variant.id): 2
        }

        session.save()

        self.client.post(
            '/orders/checkout/',
            {
                'address': 'Calicut'
            }
        )

        self.assertEqual(
            OrderItem.objects.count(),
            1
        )
        
    def test_cancel_pending_order(self):

        order = Order.objects.create(
            buyer=self.user,
            shipping_address='Calicut',
            status='pending'
            )

        self.client.login(
            username='buyer',
            password='test123'
        )

        response = self.client.post(
            f'/api/orders/{order.id}/cancel/'
        )

        self.assertEqual(
            response.status_code,
            200
            )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            'cancelled'
            )


    def test_cancel_after_24_hours(self):

        order = Order.objects.create(
            buyer=self.user,
            shipping_address='Calicut',
            status='pending'
            )

        order.created_at = timezone.now() - timedelta(days=2)
        order.save()

        self.client.login(
            username='buyer',
            password='test123'
            )

        response = self.client.post(
            f'/api/orders/{order.id}/cancel/'
            )

        self.assertEqual(
            response.status_code,
            403
            )