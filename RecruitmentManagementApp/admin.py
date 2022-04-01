from django.contrib import admin
from . import models


# Register your models here.
class StatusModel(admin.ModelAdmin):
    # fields = ('status', 'statusOrder',)  # Add other fields here
    list_display = ('id', 'status', 'statusOrder',)

    # list_editable = ('status',)

    class Meta:
        order = ['status']


class JobModel(admin.ModelAdmin):
    # fields = ('status', 'statusOrder',)  # Add other fields here
    list_display = ('id', 'user', 'jobTitle', 'jobType', 'department',)

    # list_editable = ('jobTitle',)

    class Meta:
        order = ['status']


class UserApplicationModel(admin.ModelAdmin):
    # fields = ('status', 'statusOrder',)  # Add other fields here
    list_display = ('id', 'userId', 'jobPostId', 'jobProgressStatus', 'appliedDate')

    # list_editable = ('jobTitle',)

    class Meta:
        order = ['id']


admin.site.register(models.JobPostModel, JobModel)  # job post model
admin.site.register(models.UserJobAppliedModel, UserApplicationModel)  # job application model
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
# Candidate Feedback during joining
admin.site.register(models.CandidateJoiningFeedbackModel)
# References application
admin.site.register(models.ReferenceQuestionsModel)
admin.site.register(models.ReferenceResponseInformationView)
admin.site.register(models.ReferencesQuestionResponseModel)
