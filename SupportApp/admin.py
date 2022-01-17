from django.contrib import admin
from SupportApp import models

# Register your models here.
admin.site.register(models.TicketReasonModel)
admin.site.register(models.TicketingForSupportModel)
admin.site.register(models.ServiceModel)
admin.site.register(models.SupportMessageModel)
