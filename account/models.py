from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from core.modelsMixin import TimestampMixin

class ACCOUNT_TYPE(models.IntegerChoices):
    PERSONAL = 0, 'Personal'
    MEMBER = 1, 'Member'
    GUEST = 2, 'Guest'
    DEVELOPER = 3, 'Developer' #

class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, acct_type=ACCOUNT_TYPE.MEMBER, **extra_fields ):
        if not email:
            raise ValueError("the Email filed must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, account_type=acct_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username=username, email=email, password=password, acct_type=ACCOUNT_TYPE.PERSONAL, **extra_fields)

    def create_member(self, username, email, password=None, **extra_fields):
        return self.create_user(username=username, email=email, password=password,  acct_type=ACCOUNT_TYPE.MEMBER, **extra_fields)

    def create_guest(self, username, email, password=None, **extra_fields):
        return self.create_user(username=username, email=email, password=password, acct_type=ACCOUNT_TYPE.GUEST, **extra_fields)

    def create_developer(self, username, email, password=None, **extra_fields):
        return self.create_user(username=username, email=email, password=password, acct_type=ACCOUNT_TYPE.DEVELOPER, **extra_fields)

class Account(AbstractUser):
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE.choices, default=ACCOUNT_TYPE.MEMBER)
    phone = models.CharField(max_length=13, blank=True, null=True)

    objects = AccountManager()

    def __str__(self):
        return f"{self.username}"

    
class ADDRESS_TYPE(models.IntegerChoices):
    BILLING = 0, 'Billing'
    SHIPPING = 1, 'Shipping'
    BOTH = 2, 'Both'

class Address(TimestampMixin, models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.SmallIntegerField(choices=ADDRESS_TYPE, default=ADDRESS_TYPE.BILLING)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account', 'street_address', 'apartment', 'city', 'state', 'postal_code', 'country'],
                name='unique_address_per_user'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.account_id:
            raise ValidationError('Account must be provided for an address.')

        # ensure unique address per user
        if Address.objects.filter(
            account=self.account,
            street_address=self.street_address,
            apartment=self.apartment,
            city=self.city,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country
        ).exists():
            raise ValidationError("This address already exists for this user.")
        super().save(*args, **kwargs)
