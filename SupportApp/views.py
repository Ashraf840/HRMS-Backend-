from rest_framework import generics
from SupportApp import serializer, models


# Create your views here.
class SupportTicketView(generics.CreateAPIView):
    serializer_class = serializer.SupportTicketSerializer
    queryset = models.TicketingForSupportModel.objects.all()
