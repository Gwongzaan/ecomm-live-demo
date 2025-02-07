from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view
from api_v1.docs import customer_register_schema, login_customer_schema, refresh_token_schema

User = get_user_model()

@extend_schema_view(post=customer_register_schema)
class CustomerRegisterView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': "username already exists"}, status=status.HTTP_302_FOUND)

        User.objects.create_member(username=username, password=password, email=email)

        return Response({"message": 'User registered successfully'}, status=status.HTTP_201_CREATED)

@extend_schema_view(post=login_customer_schema)
class LoginTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny, ]


@extend_schema_view(post=refresh_token_schema)
class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny, ]

