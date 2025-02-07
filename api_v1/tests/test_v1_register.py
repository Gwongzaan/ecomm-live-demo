from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker

User = get_user_model()

class RegisterCustomerTest(APITestCase):

    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.password = self.fake.password()
        self.email = self.fake.email()
        
        
        self.data = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
        }

        self.register_url = reverse('v1:register')


    def test_register_new_customer(self):

        response = self.client.post(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "User registered successfully")
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_register_new_customer_method_not_allowed(self):
        response = self.client.get(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_existing_customer(self):
        User.objects.create_member(username=self.username, email=self.email, password=self.password)
        response = self.client.post(self.register_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.data['error'], "username already exists")
