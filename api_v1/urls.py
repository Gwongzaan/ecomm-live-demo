from django.urls import path, include
from api_v1.views import account 

urlpatterns = [
    path('auth/', include([
        path('register/', account.CustomerRegisterView.as_view(), name='register'), 
    ])), 
]
