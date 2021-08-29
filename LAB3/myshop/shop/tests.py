from django.test import TestCase
from .models import Product, Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='soda', slug='some_slug')

    def test_category_model_entry(self):
        test_category = self.category
        self.assertTrue(isinstance(test_category, Category))

    def test_category_str(self):
        test_category = self.category
        self.assertEqual(test_category.__str__(), 'soda')

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

# Create your tests here.
