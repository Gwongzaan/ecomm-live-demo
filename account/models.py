from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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

    