from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.reverse import reverse

from base.tests import BaseAPITest
from products.models import Product
from .models import List, Item

User = get_user_model()

max_page_size = 10


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


class ListAPITest(BaseAPITest):
    def _make_request_get_lists(self, **kwargs):
        url_lists_api = reverse('list-list')
        return self.client.get(url_lists_api, kwargs, format='json')

    def _make_request_create_list(self, owner, name, valid_at=None):
        url_lists_api = reverse('list-list')
        return self.client.post(url_lists_api, {'owner': owner.id, 'name': name, 'valid_at': valid_at}, format='json')

    def _make_request_delete_list(self, pk):
        url_list_api = reverse('list-detail', kwargs={'pk': pk})
        return self.client.delete(url_list_api)

    def _make_request_update_list(self, pk, **kwargs):
        url_list_api = reverse('list-detail', kwargs={'pk': pk})
        return self.client.put(url_list_api, kwargs, format='json')

    def _get_default_list_names(self):
        return [
            'Please Please Me',
            'With the Beatles',
            'A Hard Day`s Night',
            'Beatles for Sale',
            'Help!',
            'Meet the Beatles!',
            'The Beatles with Tony Sheridan and Guests',
            'Rubber Soul',
            'Yesterday and Today',
            'The Beatles Second Album',
            'Revolver',
        ]

    def test_create_list_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_create_list(self.john_lennon, 'Lennon`s Buy List')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(List.objects.count(), 1)

    def test_create_list_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_create_list(self.john_lennon, 'Lennon`s Buy List')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(List.objects.count(), 0)

    def test_delete_list_with_valid_jwt_token(self):
        my_list = List.objects.create(owner=self.john_lennon, name='Lennon`s Buy List')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_delete_list(my_list.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(List.objects.count(), 0)

    def test_delete_list_with_invalid_jwt_token(self):
        my_list = List.objects.create(owner=self.john_lennon, name='Lennon`s Buy List')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_delete_list(my_list.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(List.objects.count(), 1)

    def test_delete_list_with_other_user_token(self):
        my_list = List.objects.create(owner=self.john_lennon, name='Lennon`s Buy List')
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_delete_list(my_list.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(List.objects.count(), 1)

    def test_update_list_with_valid_jwt_token(self):
        my_list = List.objects.create(owner=self.john_lennon, name='Lennon`s Buy List')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_update_list(my_list.pk, name='Yoko`s Buy List')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(List.objects.get(pk=my_list.pk).name, 'Yoko`s Buy List')

    def test_update_list_with_invalid_jwt_token(self):
        my_list = List.objects.create(owner=self.john_lennon, name='Lennon`s Buy List')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_update_list(my_list.pk, name='Yoko`s Buy List')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(List.objects.get(pk=my_list.pk).name, 'Yoko`s Buy List')

    def test_update_list_with_other_user_token(self):
        my_list = List.objects.create(owner=self.john_lennon, name='Lennon`s Buy List')
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_update_list(my_list.pk, name='Yoko`s Buy List')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(List.objects.get(pk=my_list.pk).name, 'Yoko`s Buy List')

    def test_list_lists_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_list(self.john_lennon, name)
        response = self._make_request_get_lists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(self._get_default_list_names()))
        self.assertIsNone(data['previous'])
        self.assertIsNotNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), max_page_size)

    def test_list_lists_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_list(self.john_lennon, name)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_get_lists()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_lists_with_other_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_list(self.john_lennon, name)
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_get_lists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), 0)

    def test_list_lists_with_searches(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_list(self.john_lennon, name)
        search_key = 'Beatles'
        filtered_names = list(filter(lambda _name: search_key in _name, self._get_default_list_names()))
        response = self._make_request_get_lists(search='Beatles')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(filtered_names))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), len(filtered_names))

    def test_list_lists_with_ordering(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_list(self.john_lennon, name)
        sorted_names = sorted(self._get_default_list_names())
        response = self._make_request_get_lists(ordering='name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(self._get_default_list_names()))
        self.assertIsNone(data['previous'])
        self.assertIsNotNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), max_page_size)
        for i, result in enumerate(results):
            self.assertEqual(result['name'], sorted_names[i])


class ItemAPITest(BaseAPITest):
    def setUp(self):
        super(ItemAPITest, self).setUp()
        self._create_paul_mccartney()
        self.john_list = List.objects.create(owner=self.john_lennon, name='John`s List')
        self.yoko_list = List.objects.create(owner=self.john_lennon, name='Yoko`s List')
        self.paul_list = List.objects.create(owner=self.paul_mccartney, name='Paul`s List')
        list_of_products = [
            ('Coat', 50.20),
            ('Glasses', 40.00),
            ('Shirt', 35.50),
            ('Shoes', 500.00),
        ]
        self.products = [
            Product.objects.create(name=product[0], unit_price=product[1], owner=owner)
            for product in list_of_products for owner in [self.john_lennon, self.paul_mccartney]
        ]

    def _make_request_get_items(self, list_pk, **kwargs):
        url_items_api = reverse('item-list', kwargs={'list_pk': list_pk})
        return self.client.get(url_items_api, kwargs, format='json')

    def _make_request_create_item(self, list_pk, **kwargs):
        url_items_api = reverse('item-list', kwargs={'list_pk': list_pk})
        return self.client.post(url_items_api, kwargs, format='json')

    def _make_request_delete_item(self, list_pk, pk):
        url_item_api = reverse('item-detail', kwargs={'list_pk': list_pk, 'pk': pk})
        return self.client.delete(url_item_api)

    def _make_request_update_item(self, list_pk, pk, **kwargs):
        url_item_api = reverse('item-detail', kwargs={'list_pk': list_pk, 'pk': pk})
        return self.client.put(url_item_api, kwargs, format='json')

    def test_create_item_in_list_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_create_item(self.john_list.pk, product=self.products[0].pk, quantity=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.filter(list__owner=self.john_lennon).count(), 1)
        self.assertEqual(self.john_list.items_qty, 1)
        self.assertEqual(self.john_list.total_value, self.products[0].unit_price * 2)

    def test_create_item_in_list_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_create_item(self.john_list.pk, product=self.products[0].pk, quantity=2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Item.objects.filter(list__owner=self.john_lennon).count(), 0)
        self.assertEqual(self.john_list.items_qty, 0)

    def test_create_item_in_list_with_another_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_create_item(self.yoko_list.pk, product=self.products[0].pk, quantity=2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_item_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        item = self.john_list.add_item(self.products[0], 2)
        response = self._make_request_delete_item(self.john_list.pk, item.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.filter(list__owner=self.john_lennon).count(), 0)
        self.assertEqual(self.john_list.items_qty, 0)
        self.assertEqual(self.john_list.total_value, 0)

    def test_delete_item_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        item = self.john_list.add_item(self.products[0], 2)
        response = self._make_request_delete_item(self.john_list.pk, item.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Item.objects.filter(list__owner=self.john_lennon).count(), 1)

    def test_delete_item_with_other_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        item = self.john_list.add_item(self.products[0], 2)
        response = self._make_request_delete_item(self.john_list.pk, item.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Item.objects.filter(list__owner=self.john_lennon).count(), 1)

    def test_update_item_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        item = self.john_list.add_item(self.products[0], 2)
        response = self._make_request_update_item(self.john_list.pk, item.pk, product=self.products[1].pk, quantidade=3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.john_list.total_value, self.products[0].unit_price * 2)

    def test_update_item_with_other_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        item = self.john_list.add_item(self.products[0], 2)
        response = self._make_request_update_item(self.john_list.pk, item.pk, product=self.products[1].pk, quantidade=3)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.john_list.total_value, self.products[0].unit_price * 2)

    def test_list_items_with_valid_jwt_token(self):
        products = list(filter(lambda _product: _product.owner == self.john_lennon, self.products))
        for product in products:
            self.john_list.add_item(product, 3)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_get_items(self.john_list.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(list(products)))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), len(list(products)))

    def test_list_items_with_invalid_jwt_token(self):
        products = filter(lambda _product: _product.owner == self.john_lennon, self.products)
        for product in products:
            self.john_list.add_item(product, 3)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_get_items(self.john_list.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_lists_with_other_user_token(self):
        products = filter(lambda _product: _product.owner == self.john_lennon, self.products)
        for product in products:
            self.john_list.add_item(product, 3)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_get_items(self.john_list.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), 0)

    def test_list_lists_with_searches(self):
        products = list(filter(lambda _product: _product.owner == self.john_lennon, self.products))
        for product in products:
            self.john_list.add_item(product, 3)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        search_key = 'Coa'
        filtered_names = list(filter(lambda _product: search_key in _product.name, products))
        response = self._make_request_get_items(self.john_list.pk, search=search_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(filtered_names))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), len(filtered_names))
