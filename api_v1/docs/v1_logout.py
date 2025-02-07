from rest_framework import serializers
from drf_spectacular.utils import extend_schema 
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, OpenApiRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="The refresh token to be blacklisted.")


class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Success message indicating logout.")


class LogoutErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Error message describing the issue.")


logout_customer_schema = extend_schema(
    summary="Logout member customer",
    description=(
        "This endpoint allows a member customer to log out by invalidating their refresh token. "
        "<br>"
        "The provided refresh token is blacklisted, ensuring it cannot be reused to generate a new access token."
    ),
    request=OpenApiRequest(
        request=LogoutRequestSerializer,
        examples=[
            OpenApiExample(
                'valid example',
                description="the refresh token to be blacklisted",
                value={
                    'refresh': "fjalksdjfaoweinlkgasdkmfasd32354235kjsaf"
                }
            ),
        ]
    ),
    responses={
        200: OpenApiResponse(
            response=LogoutResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description="The response indicating a successful logout.", 
                    value={
                        "message": "Logged out successfully",
                    },
                ),
            ],
        ), 
        400: OpenApiResponse(
            response=LogoutErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description='The response when the refresh token is invalid or missting.', 
                    value={
                        "error": "Token is invalid or expired.",
                    },
                ),
            ],
        ), 
    },
    tags=["Authentication"], 
)