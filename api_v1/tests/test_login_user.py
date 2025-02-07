from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker

from django.contrib.auth import get_user_model
User = get_user_model()

class TestCustomerLogin(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.password = self.fake.password()
        self.email = self.fake.email()

        self.customer= User.objects.create_member(username=self.username, email=self.email, password=self.password)

        self.login_url = reverse('v1:login')

        self.data = {
            "username": self.username,
            'password': self.password,
        }

    def test_login_user(self):
        response = self.client.post(self.login_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_invalid_credentials(self):
        data = {
            'username': self.fake.user_name(),
            'password': self.fake.password(),
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        print(response.data['detail'])

    