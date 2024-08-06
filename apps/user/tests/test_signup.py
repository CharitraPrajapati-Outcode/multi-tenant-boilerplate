from django.urls import reverse
from django.contrib.auth.hashers import check_password

from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

from rest_framework import status

from apps.user.models import User


class SignupTestCase(TenantTestCase):

    def setUp(self):
        super().setUp()
        self.client = TenantClient(self.tenant)
        self.url = reverse('user:signup')
        User.objects.create_user(email="first@last.com", password="asd123!@#", first_name="First", last_name="Last")
    

    def test_signup(self):
        data = {
            "first_name": "first",
            "last_name": "last",
            "email": "test@gmail.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(email=data["email"]).count(), 1)
        self.assertTrue(check_password(data["password"], User.objects.get(email=data["email"]).password))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Signed up successfully. Enter OTP code sent to your email to login.'}
        )


    def test_unmatched_passwords(self):
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test@gmail.com",
            "password": "admin@123",
            "confirm_password": "admin",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'confirm_password': ["Passwords didn't match."]}
        )


    def test_unique_email(self):
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "first@last.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': ["User with this email exists."],}
        )


    def test_blank_name(self):
        data = {
            "first_name": "",
            "last_name": "",
            "email": "test@gmail.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'first_name': ["This field may not be blank."],
             'last_name': ["This field may not be blank."]}
        )


    def test_invalid_email1(self):
        data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "test@gmail..com",
            "password": "admin@123",
            "confirm_password": "admin@123",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': ["Enter a valid email address."]}
        )


    def test_blank_email(self):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "",
            "password": "admin@123",
            "confirm_password": "admin@123",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': ["This field may not be blank."]}
        )