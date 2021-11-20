from rest_framework import generics,permissions,serializers
from UserApp import models
from . import serializer
# Create your views here.
# For Admin to view all Users Information
class AllUserDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AllUserDetailsSerializer
    queryset = models.User.objects.all()
