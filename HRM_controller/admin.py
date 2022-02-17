from django.contrib import admin
from HRM_controller import models

# Register your models here.
# Survey Section
admin.site.register(models.SurveyAnswerSheetModel)
admin.site.register(models.SurveyQuestionModel)
admin.site.register(models.SurveyUserResponseModel)
# Colleague Evaluation Section
admin.site.register(models.EmployeeCriteriaModel)
admin.site.register(models.EmployeeEvaluationModel)

