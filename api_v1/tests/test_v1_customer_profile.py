from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_v1.serializers.customer import CustomerProfileSerializer
from customer.models import CustomerProfile
from account.models import Account, Address, ADDRESS_TYPE
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

        self.user = Account.objects.get(username=self.username)

        self.get_customer_profile_url = reverse("v1:customer_profile")
        self.login_url = reverse('v1:login')

    def test_get_customer_profile_unauthorized(self):
        response = self.client.get(self.get_customer_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_customer_profile_authorized(self):
        


        address_type_1 = ADDRESS_TYPE.BILLING
        street_address_1 = self.fake.street_address()
        apartment_1 =self.fake.building_number()
        city_1 = self.fake.city()
        state_1 = self.fake.state()
        postal_code_1 = self.fake.postalcode()
        country_1 = self.fake.country()

        address_type_2 = ADDRESS_TYPE.SHIPPING
        street_address_2 = self.fake.street_address()
        apartment_2 =self.fake.building_number()
        city_2 = self.fake.city()
        state_2 = self.fake.state()
        postal_code_2 = self.fake.postalcode()
        country_2 = self.fake.country()

        address_type_3 = ADDRESS_TYPE.BOTH
        street_address_3 = self.fake.street_address()
        apartment_3 =self.fake.building_number()
        city_3 = self.fake.city()
        state_3 = self.fake.state()
        postal_code_3 = self.fake.postalcode()
        country_3 = self.fake.country()

        Address.objects.create(
                account=self.user, 
                address_type=address_type_1,
                street_address=street_address_1,
                apartment = apartment_1,
                city=city_1,
                state=state_1,
                postal_code=postal_code_1,
                country=country_1
            )
        
        Address.objects.create(
                account=self.user, 
                address_type=address_type_2,
                street_address=street_address_2,
                apartment = apartment_2,
                city=city_2,
                state=state_2,
                postal_code=postal_code_2,
                country=country_2
            )

        Address.objects.create(
                account=self.user, 
                address_type=address_type_3,
                street_address=street_address_3,
                apartment = apartment_3,
                city=city_3,
                state=state_3,
                postal_code=postal_code_3,
                country=country_3
            )

        
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


        expected_data = {
            'customer': {
                'addresses': [
                    {
                        'address_type': address_type_1, 
                        'street_address': street_address_1, 
                        'apartment': apartment_1, 
                        'city': city_1, 
                        'state': state_1, 
                        'postal_code': postal_code_1, 
                        'country': country_1, 
                        'is_default': False
                    },  
                    {
                        'address_type': address_type_2, 
                        'street_address': street_address_2, 
                        'apartment': apartment_2, 
                        'city': city_2, 
                        'state': state_2, 
                        'postal_code': postal_code_2, 
                        'country': country_2, 
                        'is_default': False
                    },  
                    {
                        'address_type': address_type_3, 
                        'street_address': street_address_3, 
                        'apartment': apartment_3, 
                        'city': city_3, 
                        'state': state_3, 
                        'postal_code': postal_code_3, 
                        'country': country_3, 
                        'is_default': False
                    },  
                ],
                'username': self.username, 
                'first_name': self.first_name, 
                'last_name': self.last_name, 
                'email': self.email,
            },
            'profile_picture_url': self.profile_picture_url,
        }
        self.assertEqual(response.data, expected_data)
