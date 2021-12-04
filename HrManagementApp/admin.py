from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.JobPostModel)
admin.site.register(models.UserJobAppliedModel)
admin.site.register(models.FilterQuestionsResponseModelHR)