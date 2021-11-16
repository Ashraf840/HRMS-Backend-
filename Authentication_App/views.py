from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Authentication_App.models import User
from Authentication_App import serializers
from rest_framework import generics
from rest_framework import generics, status


# Create your views here.

# generics View for List,create request
class ListCreateUserAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializers

# generic view for update,Delete, put, patch request
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializers
    lookup_field = 'pk'
