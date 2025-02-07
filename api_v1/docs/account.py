from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, extend_schema_serializer 
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from django.contrib.auth import get_user_model

User = get_user_model()

# /v1/auth/register/
class CustomerRegisterRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', )

class CustomerRegisterSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Customer registered successfully")

class CustomerRegisterErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text='Server was not able to process your requeset')

class CustomerRegisterExistResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text='Customer already exists')

customer_register_schema = extend_schema(
    summary="Register a new member customer", 
    description=(
        "This endpoint allows users to register a new account by providing"
        "a unique username, a valid email address, and a password"
        "<br>"
        "Upon successful registration, a success message is returned"
        "<br>"
        "If the username already exists, an error message is returned"
    ), 
    request=CustomerRegisterRequestSerializer,
    responses={
        201: OpenApiResponse(
            response=CustomerRegisterSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    'Valid example',
                    description="Customer registered successfully",
                    value={
                        'message': "Customer registered successfully",
                    }
                ),
            ]
        ), 
        302: OpenApiResponse(
            response=CustomerRegisterExistResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description="Username exists already",
                    value={
                        'message': 'username exists already',
                    }
                ),
            ]
        ),
        400: OpenApiResponse(
            response=CustomerRegisterErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description="Server not able handle this request",
                    value={
                        'error': 'Server not able to handle this request'
                    }
                ),
            ]
        ), 
        405: OpenApiResponse(
            response=CustomerRegisterErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description="method not allow",
                    value={
                        'error': "method not allowed",
                    }
                ),
            ] 
        ),
    }, 
    tags=['Registration', ]
)


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