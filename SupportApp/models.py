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
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE, related_name='service_support_service')
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.service.serviceName}'


class SupportMessageModel(models.Model):
    message = models.CharField(max_length=255, blank=True)
    time = models.DateTimeField(auto_now=True)
    id_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.message}'