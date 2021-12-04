from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.LevelModel)
admin.site.register(models.FieldTypeModels)
admin.site.register(models.QuestionSetModel)
admin.site.register(models.QuestionAnswerModel)
admin.site.register(models.SubmittedAnswerModel)
admin.site.register(models.JobApplyFilterQuestionModel)
# admin.site.register(models.FilterQuestionsResponseModel)

