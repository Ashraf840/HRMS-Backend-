from django.contrib import admin
from . import models


# Register your models here.
class StatusModel(admin.ModelAdmin):
    fields = ('status', 'statusOrder',)  # Add other fields here
    list_display = ('status', 'statusOrder',)

    # list_editable = ('status',)

    class Meta:
        order = ['status']


admin.site.register(models.JobPostModel)  # job post model
admin.site.register(models.UserJobAppliedModel)  # job application model
# online, practical test section
admin.site.register(models.OnlineTestModel)
admin.site.register(models.PracticalTestModel)
admin.site.register(models.PracticalTestResponseModel)
admin.site.register(models.OnlineTestResponseModel)
admin.site.register(models.JobStatusModel, StatusModel)  # job status model
# Official document, references submission section
admin.site.register(models.DocumentSubmissionModel)
admin.site.register(models.ReferenceInformationModel)
# appointment letter, signed appointment letter
admin.site.register(models.OfficialDocumentsModel)
admin.site.register(models.SignedAppointmentLetterModel)
# filter questions sections
admin.site.register(models.JobApplyFilterQuestionModel)
admin.site.register(models.FilterQuestionAnswerModel)
admin.site.register(models.FilterQuestionsResponseModelHR)
admin.site.register(models.JobFilterQuestionRadioButtonOptionModel)
