from django.db import models
from UserApp.models import User


# Create your models here.
# class SupportModel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_request_user')
#     message = models.CharField(max_length=255, blank=True)
#     id_read = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.user.full_name}, {self.message}'

