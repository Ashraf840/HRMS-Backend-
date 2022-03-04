from django.db import models
from UserApp.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    time = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def total_message(self):
        return self.message_support_ticket.filter(ticket_id=self.id).count()

    @property
    def unread_messages(self):
        messages = self.message_support_ticket.filter(ticket_id=self.id, user=self.user)
        unread = 0
        for msg in messages:
            if not msg.is_read:
                unread += 1
        return unread


    def __str__(self):
        return f'{self.ticketReason.reason}'


class SupportMessageModel(models.Model):
    ticket = models.ForeignKey(TicketingForSupportModel, on_delete=models.CASCADE,
                               related_name='message_support_ticket')
    message = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user')
    userName = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user_name')
    userImage = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @receiver(post_save, sender=TicketingForSupportModel)
    def create_support_message(sender, instance, created, **kwargs):
        if created:
            SupportMessageModel.objects.create(ticket=instance, user=instance.user, message=instance.query,
                                               userName=instance.user)

    def __str__(self):
        return f'{self.message}'


@receiver(post_save, sender=SupportMessageModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        update = TicketingForSupportModel.objects.get(id=instance.ticket.id)
        update.save()


