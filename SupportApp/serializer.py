from rest_framework import serializers
from SupportApp import models


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Ticketing for support
    """
    class Meta:
        model = models.TicketingForSupportModel
        fields = '__all__'
