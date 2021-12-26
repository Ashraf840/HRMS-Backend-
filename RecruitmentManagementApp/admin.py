from django.contrib import admin
from . import models


# Register your models here.
class StatusModel(admin.ModelAdmin):
    fields = ('status', 'statusOrder',)  # Add other fields here
    list_display = ('status', 'statusOrder',)

    # list_editable = ('status',)

    class Meta:
        order = ['status']


admin.site.register(models.JobPostModel)
admin.site.register(models.UserJobAppliedModel)
admin.site.register(models.FilterQuestionsResponseModelHR)
admin.site.register(models.OnlineTestModel)
admin.site.register(models.PracticalTestModel)
admin.site.register(models.PracticalTestResponseModel)
admin.site.register(models.OnlineTestResponseModel)
admin.site.register(models.JobStatusModel, StatusModel)
admin.site.register(models.DocumentSubmissionModel)
admin.site.register(models.ReferenceInformationModel)
