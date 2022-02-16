from django.db import models
from UserApp import models as user_model

# Create your models here.

# Month Choices
months = (
    ('jan', 'January'),
    ('feb', 'February'),
    ('mar', 'March'),
    ('apr', 'April'),
    ('may', 'May'),
    ('jun', 'June'),
    ('jul', 'July'),
    ('aug', 'August'),
    ('sep', 'September'),
    ('oct', 'October'),
    ('nov', 'November'),
    ('dec', 'December'),
)


class SurveyAnswerSheetModel(models.Model):
    answers = models.CharField(max_length=255)

    def __str__(self):
        return self.answers


class SurveyQuestionModel(models.Model):
    question = models.CharField(max_length=255)
    answers = models.ManyToManyField(SurveyAnswerSheetModel, related_name='questions_answers')

    def __str__(self):
        return self.question


class SurveyUserResponseModel(models.Model):
    user = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name='survey_response_user')
    question = models.ForeignKey(SurveyQuestionModel, on_delete=models.CASCADE, related_name='survey_response_question')
    answer = models.CharField(max_length=255)
    months = models.CharField(max_length=255, choices=months)
    ans_time = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.question} - {self.months} - {self.is_answered}'
