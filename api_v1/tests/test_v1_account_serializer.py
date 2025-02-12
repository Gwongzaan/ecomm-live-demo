from django.test import TestCase
from api_v1.serializers.account import AccountSerializer, AddressSerializer
from faker import Faker
from account.models import Address, ADDRESS_TYPE 
from django.contrib.auth import get_user_model

User = get_user_model()

class AddressSerializerTest(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.user = User.objects.create_member(username=self.username, email=self.email, password=self.password, first_name=self.first_name, last_name=self.last_name)

    def test_AddressSerializer(self):
        street_address = self.fake.street_address()

        address = Address.objects.create(
                account=self.user, 
                address_type=ADDRESS_TYPE.BILLING,
                street_address=street_address,
                apartment=self.fake.building_number(),
                city=self.fake.city(),
                state=self.fake.state(),
                postal_code=self.fake.postalcode(),
                country=self.fake.country()
            )

        s = AddressSerializer(address)

        self.assertEqual(s.data['street_address'], street_address)

class AccountSerializerTest(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.user = User.objects.create_member(username=self.username, email=self.email, password=self.password, first_name=self.first_name, last_name=self.last_name)

    def test_AccountSerializer(self):
        data = AccountSerializer(self.user).data
        self.assertEqual(data['first_name'], self.first_name)

    def test_with_multiple_addresses(self):

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

        s = AccountSerializer(self.user)

        expected_data = {
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
            'email': self.email
        }
        
        self.assertEqual(s.data, expected_data)