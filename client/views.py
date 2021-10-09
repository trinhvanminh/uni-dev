from .models import Client
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('-date_joined')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]
