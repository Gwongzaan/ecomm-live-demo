from django.urls import path, include
from api_v1.views import account 

urlpatterns = [
    path('auth/', include([
        path('register/', account.CustomerRegisterView.as_view(), name='register'), 
        path('login/', account.LoginTokenObtainPairView.as_view(), name='login'),
        path('refresh/', account.RefreshTokenView.as_view(), name='refresh-token'),
        path('logout/', account.LogoutCustomerView.as_view(), name='logout'),
    ])), 
]
