from django.test import TestCase
from account.models import Account, ACCOUNT_TYPE 
from faker import Faker

class AccountManagerTest(TestCase):
    def setUp(self):
        fake = Faker()
        self.valid_email = fake.email()
        self.valid_password = fake.password()
        self.username = fake.user_name()
        self.superuser = fake.user_name()
        self.superuser_email = fake.email()
        self.superuser_password = fake.password()

    def test_create_user(self):
        user = Account.objects.create_user(username=self.username, email=self.valid_email, password=self.valid_password)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.valid_email)
        self.assertTrue(user.check_password(self.valid_password))
        self.assertEqual(user.account_type, ACCOUNT_TYPE.MEMBER)  # Default MEMBER account type

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(username=self.username, email=None, password=self.valid_password)

    def test_create_superuser(self):
        admin = Account.objects.create_superuser(username=self.superuser, email=self.superuser_email, password=self.superuser_password)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.account_type, ACCOUNT_TYPE.PERSONAL)  # PERSONAL account type

    def test_create_member(self):
        customer = Account.objects.create_member(username=self.username, email=self.valid_email, password=self.valid_password)
        self.assertEqual(customer.account_type, ACCOUNT_TYPE.MEMBER)  # MEMBER account type

    def test_create_guest(self):
        guest = Account.objects.create_guest(username=self.username, email=self.valid_email, password=self.valid_password)
        self.assertEqual(guest.account_type, ACCOUNT_TYPE.GUEST)  # GUEST account type

    def test_create_developer(self):
        developer = Account.objects.create_developer(username=self.username, email=self.valid_email, password=self.valid_password)
        self.assertEqual(developer.account_type, ACCOUNT_TYPE.DEVELOPER)  # DEVELOPER account type
    