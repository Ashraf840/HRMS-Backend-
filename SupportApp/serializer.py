from rest_framework import serializers
from SupportApp import models


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Ticketing for support
    """

    class Meta:
        model = models.TicketingForSupportModel
        fields = '__all__'


class SupportMessageSerializer(serializers.ModelSerializer):
    """
    message based on the ticket
    """

    class Meta:
        model = models.SupportMessageModel
        fields = '__all__'

        extra_kwargs = {
            'is_read': {'read_only': True},
            'user': {'read_only': True},
            'ticket': {'read_only': True}
        }
