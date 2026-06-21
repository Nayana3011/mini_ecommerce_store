from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class StripeMockTest(TestCase):

    @patch(
        'stripe.checkout.Session.create'
    )
    def test_stripe_session_mock(self,mock_session):

        mock_session.return_value = {"id": "test123"}

        response = self.client.get(reverse('stripe_test'))

        self.assertEqual(response.status_code,200)

        mock_session.assert_called_once()