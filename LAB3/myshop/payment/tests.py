from django.test import TestCase


class pay_tests(TestCase):
    def setUp(self):
        self.response = self.client.get('/payment/')

    def test_payment_status_code(self):
        self.assertEqual(self.response.status_code, 302)
# Create your tests here.
