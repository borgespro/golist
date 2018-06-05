from django.urls import reverse
from rest_framework import status

from base.tests import BaseAPITest
from products.models import Category


max_page_size = 10


class CategoryAPITest(BaseAPITest):
    def _make_request_get_categories(self, **kwargs):
        url_lists_api = reverse('category-list')
        return self.client.get(url_lists_api, kwargs, format='json')

    def _make_request_create_category(self, owner, title, description=''):
        url_categories_api = reverse('category-list')
        return self.client.post(url_categories_api, {'owner': owner.id, 'title': title, 'description': description},
                                format='json')

    def _make_request_delete_category(self, pk):
        url_category_api = reverse('category-detail', kwargs={'pk': pk})
        return self.client.delete(url_category_api)

    def _make_request_update_category(self, pk, **kwargs):
        url_category_api = reverse('category-detail', kwargs={'pk': pk})
        return self.client.put(url_category_api, kwargs, format='json')

    def _get_default_list_names(self):
        return [
            'Clothes',
            'Toys',
            'Foods',
            'Fruits'
        ]

    def test_create_category_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_create_category(self.john_lennon, 'Clothes', 'List for buy new clothes')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().title, 'Clothes')
        self.assertEqual(Category.objects.first().description, 'List for buy new clothes')

    def test_create_category_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_create_category(self.john_lennon, 'Clothes', 'List for buy new clothes')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.count(), 0)

    def test_delete_category_with_valid_jwt_token(self):
        category = Category.objects.create(
            owner=self.john_lennon, title='Clothes', description='List for buy new clothes')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_delete_category(category.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_delete_category_with_invalid_jwt_token(self):
        category = Category.objects.create(
            owner=self.john_lennon, title='Clothes', description='List for buy new clothes')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_delete_category(category.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.count(), 1)

    def test_delete_category_with_other_user_token(self):
        category = Category.objects.create(
            owner=self.john_lennon, title='Clothes', description='List for buy new clothes')
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_delete_category(category.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Category.objects.count(), 1)

    def test_update_category_with_valid_jwt_token(self):
        category = Category.objects.create(
            owner=self.john_lennon, title='Clothes', description='List for buy new clothes')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_update_category(
            category.pk, title='Souvenir', description='List for buy new souvenirs')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get(pk=category.pk).title, 'Souvenir')
        self.assertEqual(Category.objects.get(pk=category.pk).description, 'List for buy new souvenirs')

    def test_update_category_with_invalid_jwt_token(self):
        category = Category.objects.create(
            owner=self.john_lennon, title='Clothes', description='List for buy new clothes')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_update_category(
            category.pk, title='Souvenir', description='List for buy new souvenirs')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.get(pk=category.pk).title, 'Clothes')
        self.assertEqual(Category.objects.get(pk=category.pk).description, 'List for buy new clothes')

    def test_update_category_with_other_user_token(self):
        category = Category.objects.create(
            owner=self.john_lennon, title='Clothes', description='List for buy new clothes')
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_update_category(
            category.pk, title='Souvenir', description='List for buy new souvenirs')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Category.objects.get(pk=category.pk).title, 'Clothes')
        self.assertEqual(Category.objects.get(pk=category.pk).description, 'List for buy new clothes')

    def test_list_categories_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_category(self.john_lennon, name)
        response = self._make_request_get_categories()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(self._get_default_list_names()))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), len(self._get_default_list_names()))

    def test_list_categories_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_category(self.john_lennon, name)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_get_categories()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_categories_with_other_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name in self._get_default_list_names():
            self._make_request_create_category(self.john_lennon, name)
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_get_categories()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), 0)


