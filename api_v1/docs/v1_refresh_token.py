from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, OpenApiRequest

class RefreshTokenSuccessResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text='refresh token')
    access = serializers.CharField(help_text='access token')

refresh_token_schema = extend_schema(
    summary="Refresh JWT token",
    description=(
        "Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid."
    ),
    request=OpenApiRequest(
        request=TokenRefreshSerializer,
        examples=[
            OpenApiExample(
                'valid example',
                description='request refresh token',
                value={
                    'refresh': "ksadf3234jadlwreqwek...",
                }
            ),
        ],
    ),
    responses={
        200: OpenApiResponse(
            response=RefreshTokenSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    'valid example',
                    description=(
                        "refresh tokens"
                    ),
                    value={
                        'refresh': "kaslkdfasdflkjaslkdfj",
                        'access': "asldkfj2392j4lik23j",
                    }
                ),
            ]
        ),
    }, 

    tags=['Authentication', ]
)