from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.JobPostModel)
admin.site.register(models.UserJobAppliedModel)
admin.site.register(models.FilterQuestionsResponseModelHR)
admin.site.register(models.OnlineTestModel)
admin.site.register(models.PracticalTestModel)
admin.site.register(models.PracticalTestResponseModel)
admin.site.register(models.OnlineTestResponseModel)
admin.site.register(models.JobStatusModel)
