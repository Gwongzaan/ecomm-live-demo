from rest_framework import serializers
from django.contrib.auth import get_user_model 
from account.models import Address

User = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('account', 'id', 'created_at', 'updated_at', )

class AccountSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['addresses',"username", 'first_name', 'last_name', 'email', ] 

