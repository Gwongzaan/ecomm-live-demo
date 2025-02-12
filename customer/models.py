from django.db import models
from django.contrib.auth import get_user_model

ACCOUNT = get_user_model()

class CustomerProfileManager(models.Manager):
    
    # TODO figure a way to create_member with extra_fields to account

    def create_member(self, username, password, email, **extra_fields ):
        account = ACCOUNT.objects.create_member(username=username, password=password, email=email)
        member_profile = self.create(customer=account, **extra_fields)
        return member_profile

    def create_guest(self, username, password, email, **extra_fields):
        account = ACCOUNT.objects.create_guest(username=username, password=password, email=email)
        guest_profile = self.create(customer=account, **extra_fields)
        return guest_profile


class CustomerProfile(models.Model):
    customer = models.OneToOneField(ACCOUNT, on_delete=models.CASCADE, related_name="customer_profile")
    profile_picture_url = models.URLField(max_length=200, blank=True)

    objects = CustomerProfileManager()