from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.OfficialDocStore)
admin.site.register(models.PracticalTestUserModel)
admin.site.register(models.MarkingDuringInterviewModel)
admin.site.register(models.PracticalTestMarkInputModel)
admin.site.register(models.InterviewTimeScheduleModel)
admin.site.register(models.GenerateAppointmentLetterModel)
admin.site.register(models.FinalSalaryNegotiationModel)
admin.site.register(models.CommentsOnDocumentsModel)
admin.site.register(models.PolicySentModel)



