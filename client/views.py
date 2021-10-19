from .models import Client
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ClientSerializer
from dj_rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from dj_rest_auth.app_settings import (
    JWTSerializer, TokenSerializer, create_token,
)
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('-date_joined')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {
            "message": f"user {request.data['email']} created",
            "status": 201,
        }
        response.data = custom_data
        return response
