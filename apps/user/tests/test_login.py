from django.urls import reverse

from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from rest_framework.test import APITestCase

from apps.user.models import User


class TestLoginLogout(TenantTestCase, APITestCase):
    def setUp(self):
        self.c = TenantClient(self.tenant)
        self.signin_url = reverse('user:login')
        self.logout_url = reverse('user:logout')
        self.user = User.objects.create_user(email="client@test.com", password="admin@123")
        self.deleted_user = User.objects.create_user(email="delete@test.com", password="admin@123")
        self.deleted_user.delete()

    def test_signin(self):
        data = {
            "email": "client@test.com",
            "password": "admin@123"
        }
        response = self.c.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'refresh')
        self.assertContains(response, 'access')

    def test_credentials_error(self):
        data = {
            "email": "client@test.com",
            "password": "admin"
        }
        response = self.c.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], "No active account found with the given credentials")

    def test_deleted_user_login(self):
        data = {
            "email": "delete@test.com",
            "password": "admin@123"
        }
        response = self.c.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'message': 'No active account found with the given credentials'})

    def login(self):
        data = {
            "email": "client@test.com",
            "password": "admin@123"
        }
        response = self.c.post(self.signin_url, data, format='json')
        return response.data

    def test_logout(self):
        login_credentials = self.login()
        data = {
            "refresh": login_credentials['refresh']
        }

        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_credentials['access']
        }
        response = self.c.post(self.logout_url, data, format='json', **headers)
        self.assertEqual(response.data, {'message': 'Successfully logged out.'})

    def test_wrong_access_token(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + 'test'
        }
        data = {
            "refresh": 'abc'
        }
        response = self.c.post(self.logout_url, data, format='json', **headers)
        error_message = {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
        self.assertEqual(response.data['messages'][0], error_message)