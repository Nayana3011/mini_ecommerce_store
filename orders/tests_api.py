from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from orders.models import Order


class OrderAPITest(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(username='buyer',password='123')

        self.order = Order.objects.create(buyer=self.user,shipping_address='Calicut')

        self.client.login(username='buyer',password='123')

    def test_order_list_api(self):

        response = self.client.get('/api/orders/')

        self.assertEqual(response.status_code,200)