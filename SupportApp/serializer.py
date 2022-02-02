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

    user = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    ticketReason = serializers.SlugRelatedField(queryset=models.TicketReasonModel.objects.all(),
                                                slug_field='reason')


    class Meta:
        model = models.TicketingForSupportModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'is_active': {'read_only': True}
        }


class SupportMessageSerializer(serializers.ModelSerializer):
    """
    message based on the ticket
    """
    user = serializers.SlugRelatedField(read_only=True, slug_field='full_name')

    class Meta:
        model = models.SupportMessageModel
        fields = '__all__'
        extra_kwargs = {
            # 'user': {'read_only': True},
            'is_read': {'read_only': True},
            'ticket': {'read_only': True},

        }
