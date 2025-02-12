from api_v1.docs.v1_customer_profile import customer_profile_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view
from customer.models import CustomerProfile 
from api_v1.serializers.customer import CustomerProfileSerializer
from rest_framework import status

@extend_schema_view(get=customer_profile_schema)
class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            customer_profile = CustomerProfile.objects.get(customer=request.user)
            data = CustomerProfileSerializer(customer_profile).data
            return Response(data=data, status=status.HTTP_200_OK)
        except CustomerProfile.DoesNotExist as e:
            return Response({"error": "Customer Profile Not Found"}, status=status.HTTP_404_NOT_FOUND)