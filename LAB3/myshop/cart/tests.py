from decimal import Decimal

from django.test import TestCase

from cart.cart import Cart
from shop.models import Product, Category


# Create your tests here.


class CartServiceTest(TestCase):
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
        self.product2 = Product.objects.create(category=self.category,
                                               name='Monster 2',
                                               slug='some_slug',
                                               image='some',
                                               description='best energetic',
                                               price=3.20,
                                               available=True,
                                               created='10.10.2001',
                                               updated='10.10.2001')
        self.cart = Cart.__new__(Cart)
        Cart.__init__(self.cart, self.client)
        self.response = self.client.get('/cart/')

    def test_add(self):
        previous_value = self.cart.__len__()
        self.cart.add(self.product)
        self.assertEqual(self.cart.__len__(), previous_value + 1)

    def test_add_and_override_quantity(self):
        counter = 6
        self.add_multiple(counter)
        self.cart.add(self.product, 6, True)
        self.assertEqual(self.cart.__len__(), counter)

    def test_add_multiple(self):
        counter = 7
        previous_value = self.cart.__len__()
        self.add_multiple(counter)
        self.assertEqual(self.cart.__len__(), previous_value + counter)

    def test_add_multiple_with_quantity(self):
        counter = 7
        previous_value = self.cart.__len__()
        self.cart.add(self.product, counter)
        self.assertEqual(self.cart.__len__(), previous_value + counter)

    def test_add_different(self):
        previous_value = self.cart.__len__()
        self.cart.add(self.product)
        self.cart.add(self.product2)
        self.assertEqual(self.cart.__len__(), previous_value + 2)

    def test_remove(self):
        self.cart.add(self.product)
        previous_value = self.cart.__len__()
        self.cart.remove(self.product)
        self.assertEqual(self.cart.__len__(), previous_value - 1)

    def test_save(self):
        self.cart.save()
        self.assertTrue(self.cart.session.modified)

    def test_clear(self):
        self.cart.add(self.product)
        self.cart.clear()
        self.assertEqual(self.cart.session.modified, True)

    def test_sum(self):
        pr1 = Decimal(str(self.product.price))
        pr2 = Decimal(str(self.product2.price))
        self.cart.add(self.product)
        self.cart.add(self.product2)
        self.assertEqual(pr1 + pr2, self.cart.get_total_price())

    def add_multiple(self, counter):
        for i in range(1, counter + 1):
            self.cart.add(self.product)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

