from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime

from products.models import Product
from .models import List

User = get_user_model()

from django.db.models import Sum


class ListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_if_list_is_active(self):
        tomorrow = datetime.now() + timedelta(days=1)
        yesterday = datetime.now() - timedelta(days=1)
        my_tomorrow_list = List.objects.create(owner=self.user, name='My Test List for Tomorrow', valid_at=tomorrow)
        self.assertTrue(my_tomorrow_list.is_active)
        my_yesterday_list = List.objects.create(owner=self.user, name='My Test List for Yesterday', valid_at=yesterday)
        self.assertFalse(my_yesterday_list.is_active)

    def test_add_item(self):
        my_list = List.objects.create(owner=self.user, name='My Test List')
        # Milk
        milk_price, milk_qty = 1.99, 4
        milk = Product.objects.create(owner=self.user, name='Milk', unit_price=milk_price)
        # Cheese
        cheese_price, cheese_qty = 5.10, 9
        cheese = Product.objects.create(owner=self.user, name='Cheese', unit_price=cheese_price)
        my_list.add_item(milk, milk_qty)
        self.assertEqual(my_list.items_qty, 1)
        self.assertEqual(my_list.products_qty, milk_qty)
        self.assertEqual(my_list.total_value, milk_qty * milk_price)
        my_list.add_item(cheese, cheese_qty)
        self.assertEqual(my_list.items_qty, 2)
        self.assertEqual(my_list.products_qty, milk_qty + cheese_qty)
        self.assertEqual(my_list.total_value, milk_qty * milk_price + cheese_qty * cheese_price)



