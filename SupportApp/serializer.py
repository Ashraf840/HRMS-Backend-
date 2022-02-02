from rest_framework import serializers
from SupportApp import models


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Ticketing for support
    """
    messages_count = serializers.SerializerMethodField('_checked')

    def _checked(self, filters):
        total = getattr(filters, 'total_message')
        return total

    ticketReason = serializers.SlugRelatedField(queryset=models.TicketReasonModel.objects.all(),
                                                slug_field='reason')

    service = serializers.SlugRelatedField(queryset=models.ServiceModel.objects.all(),
                                           slug_field='serviceName')

    class Meta:
        model = models.TicketingForSupportModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


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
            'ticket': {'read_only': True},

        }
