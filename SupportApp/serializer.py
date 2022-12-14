from rest_framework import serializers
from SupportApp import models


class TicketReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketReasonModel
        fields = '__all__'


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Ticketing for support
    """
    messages_count = serializers.SerializerMethodField('_checked')
    unread_message = serializers.BooleanField(source='unread_messages', read_only=True)

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

    user = serializers.SlugRelatedField(read_only=True, slug_field='id')
    userName = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = models.SupportMessageModel
        fields = '__all__'
        extra_kwargs = {
            'userImage': {'read_only': True},
            'is_read': {'read_only': True},
            'ticket': {'read_only': True},

        }


class SupportTicketCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketingForSupportModel
        fields = ['is_active']
