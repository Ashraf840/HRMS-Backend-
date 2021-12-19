from django.db import models
from UserApp.models import User
from RecruitmentManagementApp.models import PracticalTestModel


# Create your models here.

class PracticalTestUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_test_user')
    practicalTestInfo = models.ForeignKey(PracticalTestModel, on_delete=models.CASCADE,
                                          related_name='practical_test_info')
    duration = models.IntegerField(blank=True, default=2)

    def __str__(self):
        return f'{self.user}, {self.practicalTestInfo}'
