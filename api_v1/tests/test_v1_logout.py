from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class LogoutTest(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.password = self.fake.password()
        self.email = self.fake.email()

        self.login_data = {
            'username': self.username,
            'password': self.password,
        }

        self.user = User.objects.create_member(username=self.username, password=self.password, email=self.email)

        self.logout_url = reverse("v1:logout")
        self.login_url = reverse('v1:login')



    def test_logout_customer(self):
        login_response = self.client.post(self.login_url, self.login_data)
        refresh_token = login_response.data['refresh']

        logout_data = {'refresh': refresh_token}
        logout_response = self.client.post(self.logout_url, logout_data)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn('message', logout_response.data)
        self.assertEqual(logout_response.data['message'], 'logged out successfully')
        
    def test_logout_with_invalid_token(self):
        self.client.post(self.login_url, self.login_data)

        invalid_token = uuid.uuid4()
        logout_data = {'refresh': invalid_token}
        response = self.client.post(self.logout_url, logout_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)