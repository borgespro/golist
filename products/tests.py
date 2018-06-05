from django.urls import reverse
from rest_framework import status

from base.tests import BaseAPITest
from products.models import Category, Product

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


class ProductAPITest(BaseAPITest):
    def _make_request_get_products(self, **kwargs):
        url_products_api = reverse('product-list')
        return self.client.get(url_products_api, kwargs, format='json')

    def _make_request_create_product(self, **kwargs):
        url_products_api = reverse('product-list')
        return self.client.post(url_products_api, kwargs, format='json')

    def _make_request_delete_product(self, pk):
        url_product_api = reverse('product-detail', kwargs={'pk': pk})
        return self.client.delete(url_product_api)

    def _make_request_update_product(self, pk, **kwargs):
        url_product_api = reverse('product-detail', kwargs={'pk': pk})
        return self.client.put(url_product_api, kwargs, format='json')

    def _get_default_list_of_products(self):
        dairy_products = Category.objects.create(owner=self.john_lennon, title='Dairy Products')
        meat = Category.objects.create(owner=self.john_lennon, title='Meat')

        return [
            ('Milk Type A', 5.99, dairy_products),
            ('Milk Type B', 4.99, dairy_products),
            ('Milk Type C', 3.99, dairy_products),
            ('Milk Type D', 2.99, dairy_products),
            ('American Cheese', 1.00, dairy_products),
            ('Italian Cheese', 1.00, dairy_products),
            ('Pork', 1.00, meat),
            ('Chicken fry', 1.00, meat),
            ('Beef', 1.00, meat),
            ('Product Without Category 1', 1.00, None),
            ('Product Without Category 2', 1.00, None),
            ('Product Without Category 3', 1.00, None),
            ('Product Without Category 4', 1.00, None),
        ]

    def test_create_product_with_category_and_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        dairy = Category.objects.create(owner=self.john_lennon, title='Dairy Products')
        response = self._make_request_create_product(owner=self.john_lennon.pk, name='Milk Type A', unit_price=5.99,
                                                     category=dairy.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_without_category_and_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_create_product(owner=self.john_lennon.pk, name='Milk Type A', unit_price=5.99)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_create_product(owner=self.john_lennon.pk, name='Milk Type A', unit_price=5.99)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_with_valid_jwt_token(self):
        product = Product.objects.create(owner=self.john_lennon, name='Milk Type A', unit_price=5.99)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_delete_product(product.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_with_invalid_jwt_token(self):
        product = Product.objects.create(owner=self.john_lennon, name='Milk Type A', unit_price=5.99)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_delete_product(product.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 1)

    def test_delete_list_with_other_user_token(self):
        product = Product.objects.create(owner=self.john_lennon, name='Milk Type A', unit_price=5.99)
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_delete_product(product.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.count(), 1)

    def test_update_product_with_valid_jwt_token(self):
        product = Product.objects.create(owner=self.john_lennon, name='Milk Type A', unit_price=5.99)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        response = self._make_request_update_product(product.pk, name='Milk Type B', unit_price=4.50)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(pk=product.pk).name, 'Milk Type B')
        self.assertEqual(Product.objects.get(pk=product.pk).unit_price, 4.50)

    def test_update_product_with_invalid_jwt_token(self):
        product = Product.objects.create(owner=self.john_lennon, name='Milk Type A', unit_price=5.99)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_update_product(product.pk, unit_price=4.50)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.get(pk=product.pk).unit_price, 5.99)

    def test_update_product_with_other_user_token(self):
        product = Product.objects.create(owner=self.john_lennon, name='Milk Type A', unit_price=5.99)
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_update_product(product.pk, unit_price=4.50)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.get(pk=product.pk).unit_price, 5.99)

    def test_list_products_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name, price, category in self._get_default_list_of_products():
            self._make_request_create_product(name=name, unit_price=price, category=category.id if category else None)
        response = self._make_request_get_products()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(self._get_default_list_of_products()))
        self.assertIsNone(data['previous'])
        self.assertIsNotNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), max_page_size)

    def test_list_lists_with_invalid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name, price, category in self._get_default_list_of_products():
            self._make_request_create_product(name=name, unit_price=price, category=category.id if category else None)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token[:-1])
        response = self._make_request_get_products()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_lists_with_other_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name, price, category in self._get_default_list_of_products():
            self._make_request_create_product(name=name, unit_price=price, category=category.id if category else None)
        self._create_paul_mccartney()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.paul_mccartney_token)
        response = self._make_request_get_products()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), 0)

    def test_list_lists_with_search_by_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name, price, category in self._get_default_list_of_products():
            self._make_request_create_product(name=name, unit_price=price, category=category.id if category else None)
        search_name = 'Milk'
        filtered_names = list(filter(lambda product: search_name in product[0], self._get_default_list_of_products()))
        response = self._make_request_get_products(search=search_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(filtered_names))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), len(filtered_names))

    def test_list_lists_with_filter_by_category(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name, price, category in self._get_default_list_of_products():
            self._make_request_create_product(name=name, unit_price=price, category=category.id if category else None)
        category_name = 'Meat'
        filtered_names = list(filter(lambda product: product[2] and product[2].title == category_name,
                                     self._get_default_list_of_products()))
        response = self._make_request_get_products(category=category_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(filtered_names))
        self.assertIsNone(data['previous'])
        self.assertIsNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), len(filtered_names))

    def test_list_lists_with_ordering(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.john_lennon_token)
        for name, price, category in self._get_default_list_of_products():
            self._make_request_create_product(name=name, unit_price=price, category=category.id if category else None)
        sorted_names = sorted([_name for _name, _price, _category in self._get_default_list_of_products()])
        response = self._make_request_get_products(ordering='name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['count'], len(sorted_names))
        self.assertIsNone(data['previous'])
        self.assertIsNotNone(data['next'])
        results = data['results']
        self.assertEqual(len(results), max_page_size)
        for i, result in enumerate(results):
            self.assertEqual(result['name'], sorted_names[i])
