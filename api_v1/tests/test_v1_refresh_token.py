from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class RefreshTokenTest(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.password = self.fake.password()
        self.email = self.fake.email()
        self.login_url = reverse('v1:login')
        self.refresh_url = reverse("v1:refresh-token")
        self.user = User.objects.create_member(username=self.username, password=self.password, email=self.email)
        self.login_data = {
            'username': self.username,
            'password': self.password,
        }

    def test_refresh_token(self):
        login_response = self.client.post(self.login_url, self.login_data)
        refresh_token = login_response.data['refresh']

        refresh_data = {"refresh": refresh_token}
        refresh_response = self.client.post(self.refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK )
        self.assertIn('access', refresh_response.data)