from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from api_v1.serializers.customer import CustomerProfileSerializer
from faker import Faker

fake = Faker()

class CustomerProfileRequestSerializer(serializers.Serializer):
    username = serializers.CharField() 

class CustomerProfileResponseSerializer(serializers.Serializer):
    pass

class CustomerProfileResponseNotFoundSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Customer Profile Not Found")

class CustomerProfileResponseUnauthorizedSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Unauthorized Access")

customer_profile_schema = extend_schema(
    summary="Retrieve customer profile data",
    description=(
        "This endpoint retrieve customer's profile data"
    ),
    request=CustomerProfileRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=CustomerProfileSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description=(
                        "customer profile data"
                        ),
                    value={
                        "customer": {
                            "username": fake.user_name(), 
                            "first_name": fake.first_name(), 
                            "last_name": fake.last_name(), 
                            "email": fake.email(),    
                        },
                        "profile_picture_url": fake.image_url(), 
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            response=CustomerProfileResponseNotFoundSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description=(
                        "customer profile not found"
                    ),
                    value = {
                        "error": "Customer Profile Not Found",
                    }
                ),
            ]
        ),
        401: OpenApiResponse(
            response=CustomerProfileResponseUnauthorizedSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description=(
                        "unauthorized access"
                    ),
                    value={
                        "error": "Unauthorized access",
                    }
                ),
            ]
        ),
    }, 
    tags=['Customer', ]
)
