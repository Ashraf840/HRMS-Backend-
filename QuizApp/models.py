from django.db import models

import UserApp.models
from UserApp.models import UserDepartmentModel


# Create your models here.
class FieldTypeModels(models.Model):
    fieldType = models.CharField(verbose_name='Field Type', max_length=50)

    class Meta:
        verbose_name_plural = 'Field Type'

    def __str__(self):
        return f'{self.fieldType}'


class LevelModel(models.Model):
    levelName = models.CharField(verbose_name='Level', max_length=50)

    class Meta:
        verbose_name_plural = 'Questions Level'

    def __str__(self):
        return f'{self.levelName}'


class QuestionSetModel(models.Model):
    # author = models.ForeignKey(UserApp.models.User,on_delete=models.CASCADE,related_name='question_author')
    fieldType = models.ForeignKey(FieldTypeModels, on_delete=models.CASCADE, related_name='question_field_type')
    department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='department_name')
    level = models.ForeignKey(LevelModel, on_delete=models.CASCADE, related_name='question_level')
    question = models.CharField(max_length=255, verbose_name='question')

    class Meta:
        verbose_name_plural = 'Question Set'

    def __str__(self):
        return f'{self.fieldType}, {self.question}'


class QuestionAnswerModel(models.Model):
    question = models.OneToOneField(QuestionSetModel, on_delete=models.CASCADE, related_name='question_answer')
    qusAnswer = models.CharField(max_length=255, verbose_name='Question Answer')

    class Meta:
        verbose_name_plural = 'Question Answer'

    def __str__(self):
        return f'{self.question}, {self.qusAnswer}'


class SubmittedAnswerModel(models.Model):
    question = models.ForeignKey(QuestionSetModel, on_delete=models.CASCADE, related_name='submitted_question')
    # correctAnswer = models.ForeignKey(QuestionAnswerModel, on_delete=models.CASCADE, related_name='correct_answer')
    user = models.ForeignKey(UserApp.models.User, on_delete=models.CASCADE, related_name='submitted_by')
    givenAnswer = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = 'Submitted Answer'

    def __str__(self):
        return f'{self.user}, {self.givenAnswer}'


# ============job apply filter questions section============

class JobApplyFilterQuestionModel(models.Model):
    fieldType = models.ForeignKey(FieldTypeModels, on_delete=models.CASCADE, related_name='filter_question_field_type')
    department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='filter_department_name')
    question = models.CharField(max_length=255, verbose_name='filter_question')

    class Meta:
        verbose_name_plural = 'Filter Question List'

    def __str__(self):
        return f'{self.fieldType}, {self.question}'


class FilterQuestionAnswerModel(models.Model):
    """
    Filter question answer will be stored here for check and select candidate for next stage
    """

    question = models.OneToOneField(JobApplyFilterQuestionModel,on_delete=models.CASCADE,
                                    related_name='job_apply_filter_question_answer')
    answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.answer}'


# class FilterQuestionsResponseModel(models.Model):
#     questions = models.ForeignKey(JobApplyFilterQuestionModel, on_delete=models.CASCADE,
#                                   related_name='filter_questions')
#     response = models.CharField(max_length=255, blank=True)
#     user = models.ForeignKey(UserApp.models.User, on_delete=models.CASCADE, related_name='response_by')
#     # jobPost = models.ForeignKey(JobPostModel,on_delete=models.CASCADE,related_name='job_info')
#
#     class Meta:
#         verbose_name_plural = 'Filter Question Response'
#
#     def __str__(self):
#         return f'{self.questions}, {self.response}'
