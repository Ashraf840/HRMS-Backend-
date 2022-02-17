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

ratings = (
    (1, 'Strongly Disagree'),
    (2, 'Disagree'),
    (3, 'Uncertain'),
    (4, 'Agree'),
    (5, 'Strongly Agree'),
)


# Survey Section
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
    ans_time = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.question} - {self.ans_time.month}/{self.ans_time.year} - {self.is_answered}'


# Colleague Evaluation Section

class EmployeeCriteriaModel(models.Model):
    criteria = models.CharField(max_length=255)

    def __str__(self):
        return self.criteria


class EmployeeEvaluationModel(models.Model):
    sender_user = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name='evaluation_sender_user')
    receiver_user = models.ForeignKey(user_model.User, on_delete=models.CASCADE,
                                      related_name='evaluation_receiver_user')
    criteria = models.ForeignKey(EmployeeCriteriaModel, on_delete=models.CASCADE, related_name='evaluation_criteria')
    ratings = models.CharField(max_length=255, choices=ratings)
    rating_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.sender_user} - {self.receiver_user} - {self.ratings} - {self.rating_date.month}/{self.rating_date.year}'


# Announcement and Notice
class AnnouncementModel(models.Model):
    department = models.ManyToManyField(user_model.UserDepartmentModel, related_name='announcement_department')
    message = models.CharField(max_length=255)


class NoticeModel(models.Model):
    department = models.ManyToManyField(user_model.UserDepartmentModel, related_name='notice_department')
    title = models.CharField(max_length=255)
    message = models.TextField()
    attachment = models.FileField()
