from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_v1.serializers.customer import CustomerProfileSerializer
from customer.models import CustomerProfile
from account.models import Account
from faker import Faker

class CustomerProfileSerializerTest(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.profile_picture_url = self.fake.image_url()

        self.customer_profile =  CustomerProfile.objects.create_member(username=self.username, email=self.email, password=self.password, profile_picture_url=self.profile_picture_url)
        self.customer_profile.customer.first_name = self.first_name
        self.customer_profile.customer.last_name = self.last_name
        self.customer_profile.customer.save()
        

    def test_CustomerProfileSerializer(self):
        cps = CustomerProfileSerializer(self.customer_profile)
        self.assertEqual(cps.data['customer']['last_name'], self.last_name)


class CutomerProfileTest(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.profile_picture_url = self.fake.image_url()

        self.customer_profile =  CustomerProfile.objects.create_member(username=self.username, email=self.email, password=self.password, profile_picture_url=self.profile_picture_url)
        self.customer_profile.customer.first_name = self.first_name
        self.customer_profile.customer.last_name = self.last_name
        self.customer_profile.customer.save()

        self.get_customer_profile_url = reverse("v1:customer_profile")
        self.login_url = reverse('v1:login')

    def test_get_customer_profile_unauthorized(self):
        response = self.client.get(self.get_customer_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_customer_profile_authorized(self):
        login_data = {
            "username": self.username,
            "password": self.password,
        }

        login_response = self.client.post(self.login_url, data=login_data)
        
        headers = {
            "Authorization": f"Bearer {login_response.data['access']}"
        }

        response = self.client.get(self.get_customer_profile_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer']['first_name'], self.first_name)
        self.assertEqual(response.data['profile_picture_url'], self.profile_picture_url)
