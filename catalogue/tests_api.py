from django.test import TestCase
from django.contrib.auth.models import User
from catalogue.models import Category, Product
from rest_framework.test import APIClient
from catalogue.models import Review


class ProductAPITest(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(username='seller',password='123')

        self.category = Category.objects.create(name='Mobile')

        self.product = Product.objects.create(
            name='Samsung M30',
            description='Phone',
            category=self.category,
            seller=self.user
        )

    def test_product_list_api(self):

        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code,200)

    def test_product_detail_api(self):

        response = self.client.get(f'/api/products/{self.product.slug}/')

        self.assertEqual(response.status_code,200)

    def test_product_filter_by_category(self):

        response = self.client.get('/api/products/?category=Mobile')

        self.assertEqual(response.status_code,200)
        

class ReviewAPITest(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(username='buyer',password='123')

        self.category = Category.objects.create(name='Mobile')

        self.product = Product.objects.create(
            name='Phone',
            description='Test',
            category=self.category,
            seller=self.user
        )

        self.client.login(
            username='buyer',
            password='123'
        )

    def test_review_create(self):

        response = self.client.post(
            '/api/reviews/',
            {
                'product': self.product.id,
                'rating': 5,
                'comment': 'Good'
            }
        )

        self.assertEqual(response.status_code,201)

    def test_duplicate_review_not_allowed(self):

        Review.objects.create(
            product=self.product,
            buyer=self.user,
            rating=5,
            comment='Good'
        )

        response = self.client.post(
            '/api/reviews/',
            {
                'product': self.product.id,
                'rating': 4,
                'comment': 'Again'
            }
        )

        self.assertEqual(response.status_code,400)