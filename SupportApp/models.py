from django.db import models
from UserApp.models import User


# Create your models here.
class TicketReasonModel(models.Model):
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.reason}'


class ServiceModel(models.Model):
    serviceName = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.serviceName}'


class TicketingForSupportModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_request_user')
    ticketReason = models.ForeignKey(TicketReasonModel, on_delete=models.CASCADE, related_name='ticketing_reason')
    # service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE, related_name='service_support_service')
    query = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def total_message(self):
        return self.message_support_ticket.filter(ticket_id=self.id).count()

    def __str__(self):
        return f'{self.ticketReason.reason}'


class SupportMessageModel(models.Model):
    ticket = models.ForeignKey(TicketingForSupportModel, on_delete=models.CASCADE,
                               related_name='message_support_ticket')
    message = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user')
    time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.message}'
