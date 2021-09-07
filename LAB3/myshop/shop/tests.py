from django.test import TestCase, SimpleTestCase
from .models import Product, Category
from django.contrib.auth.models import User
from django.urls import reverse


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='soda', slug='some_slug')

    def test_category_model_entry(self):
        test_category = self.category
        self.assertTrue(isinstance(test_category, Category))

    def test_category_str(self):
        test_category = self.category
        self.assertEqual(test_category.__str__(), 'soda')

    def test_category_absolute_url(self):
        test_category = self.category
        self.assertEqual(test_category.get_absolute_url(), '/some_slug/')

    def test_slug_max_length(self):
        test_category = self.category
        max_len = test_category._meta.get_field('slug').max_length
        self.assertEqual(max_len, 200)

    def test_name_max_length(self):
        test_category = self.category
        max_len = test_category._meta.get_field('name').max_length
        self.assertEqual(max_len, 200)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='soda', slug='some_slug')
        self.product = Product.objects.create(category=self.category,
                                              name='Monster',
                                              slug='some_slug',
                                              image='some',
                                              description='best energetic',
                                              price=3.20,
                                              available=True,
                                              created='10.10.2001',
                                              updated='10.10.2001')

    def test_product_entry(self):
        test_product = self.product
        self.assertTrue(isinstance(test_product, Product))

    def test_product_str(self):
        test_product = self.product
        self.assertEqual(test_product.__str__(), 'Monster')

    def test_product_absolute_url(self):
        test_product = self.product
        self.assertEqual(test_product.get_absolute_url(), '/29/some_slug/')

    def test_slug_max_length(self):
        test_product = self.product
        max_len = test_product._meta.get_field('slug').max_length
        self.assertEqual(max_len, 200)

    def test_name_max_length(self):
        test_product = self.product
        max_len = test_product._meta.get_field('name').max_length
        self.assertEqual(max_len, 200)

    def test_price_max_digits(self):
        test_product = self.product
        max_digits = test_product._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 10)

    def test_price_dec_places(self):
        test_product = self.product
        dec_places = test_product._meta.get_field('price').decimal_places
        self.assertEqual(dec_places, 2)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test', password='Test')
        self.user.save()
        self.response = self.client.get('/login/')

    def test_login_status_code(self):
        resp = self.client.post('/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(resp.status_code, 200)

    def test_login_template(self):
        self.assertTemplateUsed(self.response, 'shop/login.html')

    def test_login_contains_correct_html(self):
        self.assertContains(self.response, 'login')

    def test_login_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


class RegisterPageTests(TestCase):

    def setUp(self):
        self.response = self.client.get('/register/')

    def test_register_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_register_template(self):
        self.assertTemplateUsed(self.response, 'shop/register.html')

    def test_register_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')
# Create your tests here.
