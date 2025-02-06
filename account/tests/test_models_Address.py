from django.test import TestCase
from account.models import Address, Account, ADDRESS_TYPE
from django.core.exceptions import ValidationError
from faker import Faker

class AddressModelTest(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.username = self.fake.user_name()
        self.email = self.fake.email()
        self.password = self.fake.password()
        self.user = Account.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_create_address(self):
        street_address = self.fake.street_address()
        apartment = self.fake.building_number()
        city = self.fake.city()
        state = self.fake.state()
        postal_code = self.fake.postalcode()
        country = self.fake.country()

        address = Address.objects.create(
            account=self.user,
            address_type=ADDRESS_TYPE.BILLING,
            street_address=street_address,
            apartment=apartment,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=True
        )
        self.assertEqual(address.account, self.user)
        self.assertEqual(address.address_type, ADDRESS_TYPE.BILLING)
        self.assertEqual(address.street_address, street_address)
        self.assertEqual(address.apartment, apartment)
        self.assertEqual(address.city, city)
        self.assertEqual(address.state, state)
        self.assertEqual(address.postal_code, postal_code)
        self.assertEqual(address.country, country)
        self.assertTrue(address.is_default)

    def test_create_multiple_address(self):
        street_address = self.fake.street_address()
        apartment = self.fake.building_number()
        city = self.fake.city()
        state = self.fake.state()
        postal_code = self.fake.postalcode()
        country = self.fake.country()

        address = Address.objects.create(
            account=self.user,
            address_type=ADDRESS_TYPE.BILLING,
            street_address=street_address,
            apartment=apartment,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=True
        )
        self.assertEqual(address.account, self.user)
        self.assertEqual(address.address_type, ADDRESS_TYPE.BILLING)
        self.assertEqual(address.street_address, street_address)
        self.assertEqual(address.apartment, apartment)
        self.assertEqual(address.city, city)
        self.assertEqual(address.state, state)
        self.assertEqual(address.postal_code, postal_code)
        self.assertEqual(address.country, country)
        self.assertTrue(address.is_default)


        street_address = self.fake.street_address()
        apartment = self.fake.building_number()
        city = self.fake.city()
        state = self.fake.state()
        postal_code = self.fake.postalcode()
        country = self.fake.country()

        address = Address.objects.create(
            account=self.user,
            address_type=ADDRESS_TYPE.BILLING,
            street_address=street_address,
            apartment=apartment,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=True
        )
        self.assertEqual(address.account, self.user)
        self.assertEqual(address.address_type, ADDRESS_TYPE.BILLING)
        self.assertEqual(address.street_address, street_address)
        self.assertEqual(address.apartment, apartment)
        self.assertEqual(address.city, city)
        self.assertEqual(address.state, state)
        self.assertEqual(address.postal_code, postal_code)
        self.assertEqual(address.country, country)
        self.assertTrue(address.is_default)
        
        
    def test_duplicate_address_raise_ValidationError(self):
        street_address = self.fake.street_address()
        apartment = self.fake.building_number()
        city = self.fake.city()
        state = self.fake.state()
        postal_code = self.fake.postalcode()
        country = self.fake.country()

        Address.objects.create(
            account=self.user,
            address_type=ADDRESS_TYPE.BILLING,
            street_address=street_address,
            apartment=apartment,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=True
        )

        # Attempt to create a duplicate address
        with self.assertRaises(ValidationError):

            duplicate_address = Address.objects.create(
                account=self.user,
                address_type=ADDRESS_TYPE.BILLING,
                street_address=street_address,
                apartment=apartment,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                is_default=True
            )
            duplicate_address.save()
        
    def test_default_address_type(self):
        street_address = self.fake.street_address()
        apartment = self.fake.building_number()
        city = self.fake.city()
        state = self.fake.state()
        postal_code = self.fake.postalcode()
        country = self.fake.country()

        address = Address.objects.create(
            account=self.user,
            street_address=street_address,
            apartment=apartment,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=True
        )
        self.assertEqual(address.address_type, ADDRESS_TYPE.BILLING)

    def test_address_without_account(self):

        street_address = self.fake.street_address()
        apartment = self.fake.building_number()
        city = self.fake.city()
        state = self.fake.state()
        postal_code = self.fake.postalcode()
        country = self.fake.country()

        
        with self.assertRaises(ValidationError) as context:
            address = Address.objects.create(
                street_address=street_address,
                apartment=apartment,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                is_default=True
            )

        self.assertIn("Account must be provided for an address.", str(context.exception))
