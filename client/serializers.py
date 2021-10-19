from .models import Client
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['url', 'email', 'groups']
