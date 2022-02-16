from django.contrib import admin
from HRM_controller import models

# Register your models here.
admin.site.register(models.SurveyAnswerSheetModel)
admin.site.register(models.SurveyQuestionModel)
admin.site.register(models.SurveyUserResponseModel)
