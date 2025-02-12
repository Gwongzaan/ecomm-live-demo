from rest_framework import serializers
from customer.models import CustomerProfile
from api_v1.serializers.account import AccountSerializer

class CustomerProfileSerializer(serializers.ModelSerializer):
    customer = AccountSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['customer', 'profile_picture_url', ]
