from django.test import TestCase
from .models import Order, OrderItem
from shop.models import Product, Category

''' first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)'''

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(first_name='Maksim',
                                          last_name='Slizh',
                                          email='maxim.slizh@mail.ru',
                                          address='Panchenko 46-52',
                                          postal_code='2200447',
                                          city='Minsk',
                                          created='18.10.2001',
                                          updated='18.10.2001',
                                          paid=True,
                                          braintree_id='some id')


    def test_Order_Model_Entry(self):
        test_order = self.order
        self.assertTrue(isinstance(test_order, Order))

    def test_Order_str(self):
        test_order = self.order
        self.assertEqual(test_order.__str__(), 'Order 2')

    def test_get_total_cost(self):
        test_order = self.order
        self.assertEqual(test_order.get_total_cost(), 0)

    def test_name_Max_Length(self):
        test_order = self.order
        max_len = test_order._meta.get_field('first_name').max_length
        self.assertEqual(max_len, 50)

    def test_surname_Max_Length(self):
        test_order = self.order
        max_len = test_order._meta.get_field('last_name').max_length
        self.assertEqual(max_len, 50)

    def test_address_max_length(self):
        test_order = self.order
        max_len = test_order._meta.get_field('address').max_length
        self.assertEqual(max_len, 250)

    def test_post_max_length(self):
        test_order = self.order
        max_len = test_order._meta.get_field('postal_code').max_length
        self.assertEqual(max_len, 20)

    def test_city_max_length(self):
        test_order = self.order
        max_len = test_order._meta.get_field('city').max_length
        self.assertEqual(max_len, 100)

    def test_braintree_max_length(self):
        test_order = self.order
        max_len = test_order._meta.get_field('braintree_id').max_length
        self.assertEqual(max_len, 150)

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='soda', slug='some_slug')

        self.order = Order.objects.create(first_name='Maksim',
                                          last_name='Slizh',
                                          email='maxim.slizh@mail.ru',
                                          address='Panchenko 46-52',
                                          postal_code='2200447',
                                          city='Minsk',
                                          created='18.10.2001',
                                          updated='18.10.2001',
                                          paid=True,
                                          braintree_id='some id')

        self.product = Product.objects.create(category=self.category,
                                              name='Monster',
                                              slug='some_slug',
                                              image='some',
                                              description='best energetic',
                                              price=3.20,
                                              available=True,
                                              created='10.10.2001',
                                              updated='10.10.2001')
        self.item = OrderItem.objects.create(order=self.order,
                                             product=self.product,
                                             price=3.20,
                                             quantity=1)

    def test_model_order_item_entry(self):
        test_item = self.item
        self.assertTrue(isinstance(test_item, OrderItem))

    def test_model_order_item_str(self):
        test_item = self.item
        self.assertEqual(test_item.__str__(), '5')

    def test_model_order_item_price_max(self):
        test_item = self.item
        max_digits = test_item._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 10)

    def test_model_order_item_price_dec_places(self):
        test_item = self.item
        dec_places = test_item._meta.get_field('price').decimal_places
        self.assertEqual(dec_places, 2)

    def test_model_order_get_cost(self):
        test_item = self.item
        coast = test_item.get_cost()
        self.assertEqual(coast, 3.20)
# Create your tests here.
