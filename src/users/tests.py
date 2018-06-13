from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_login_with_valid_credentials(self):
        url_login = reverse('login')
        payload = {'username': 'john', 'password': 'johnpassword'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(response.data.get('token', False) is not None)

    def test_login_with_invalid_credentials(self):
        url_login = reverse('login')
        payload = {'username': 'lennon', 'password': 'wrongpassword'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(response.data.get('non_field_errors', None) is not None)

    def test_login_with_invalid_payload(self):
        url_login = reverse('login')
        payload = {'email': 'john', 'password': 'johnpassword'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(response.data.get('non_field_errors', None) is None)
        self.assertTrue(response.data.get('username', None) is not None)
