from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from django.urls import reverse

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        self.john_lennon = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.john_lennon_token = self._get_jwt_token('john', 'johnpassword')

    def _get_jwt_token(self, username, password):
        url_login = reverse('login')
        return self.client.post(url_login, {'username': username, 'password': password}, format='json').data['token']

    def _create_paul_mccartney(self):
        self.paul_mccartney = User.objects.create_user('paul', 'mccartney@thebeatles.com', 'paulpassword',
                                                       hash='PAULMCCARTNEYHASH')
        self.paul_mccartney_token = self._get_jwt_token('paul', 'paulpassword')
