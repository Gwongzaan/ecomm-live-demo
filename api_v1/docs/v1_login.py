from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginCustomerSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Customer login successfully")

class LoginCustomerErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Server not able to handle the request")


class LoginUnauthorizeResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="No active account found with the provided credentials")

login_customer_schema = extend_schema(
    summary="Login member customer",
    description=(
        "This endpoint allows users to obtain a pair of JSON Web Tokens "
        "(access and refresh tokens). "
        "<br>"
        "The access token is used for authenticating subsequent requests,"
        "while the refresh token is used "
        "to generate new access tokens when the old one expires."
    ),
    request=TokenObtainPairSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginCustomerSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description=(
                        "login suceesfully"
                    ),
                    value={
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            response=LoginUnauthorizeResponseSerializer,
            examples=[
                OpenApiExample(

                    'valid example',
                    description=(
                        "No active account found"
                    ),
                    value={
                        'detail': 'No active account found with the given credentials',
                    }
                ),
            ]
            
        )
    },
    tags=['Authentication', ]
)