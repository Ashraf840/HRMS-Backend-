import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from UserApp import models as user_model
from HRM_Admin import models as hrm_models

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


# Announcement, Notice and Complain
class AnnouncementModel(models.Model):
    department = models.ManyToManyField(user_model.UserDepartmentModel, related_name='announcement_department')
    message = models.CharField(max_length=255)


class NoticeModel(models.Model):
    department = models.ManyToManyField(user_model.UserDepartmentModel, related_name='notice_department')
    title = models.CharField(max_length=255)
    message = models.TextField()
    attachment = models.FileField()


class ComplainModel(models.Model):
    complain_at = models.ForeignKey(hrm_models.EmployeeInformationModel, on_delete=models.CASCADE,
                                    related_name='complain_employee')
    complain_reason = models.CharField(max_length=255)
    complain_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f'Complained at - {self.complain_at}'


# ==================Holiday Section==================
class HolidayModel(models.Model):
    holiday_name = models.CharField(max_length=255)
    holiday_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.holiday_name} - {self.holiday_date} - {self.is_active}'


# ==================Attendance Section ==================
# Attendance Shift, relation model

class AttendanceShiftTimeModel(models.Model):
    shift_name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.shift_name} - ({self.start_time}-{self.end_time})'


class AttendanceEmployeeRelModel(models.Model):
    employee = models.OneToOneField(hrm_models.EmployeeInformationModel, on_delete=models.SET_NULL,
                                    related_name='attendance_employee_relation', blank=True, null=True)
    registration_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.employee}, {self.registration_id}'


class AttendanceEmployeeShiftRelModel(models.Model):
    employee_relation = models.ForeignKey(AttendanceEmployeeRelModel, on_delete=models.CASCADE,
                                          related_name='attendance_employee_relation')
    shift = models.ForeignKey(AttendanceShiftTimeModel, on_delete=models.CASCADE,
                              related_name='attendance_employee_shift')

    def __str__(self):
        return f'{self.employee_relation} - {self.shift}'


class EmployeeAttendanceLogModel(models.Model):
    employee = models.ForeignKey(hrm_models.EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='employee_attendance_log')
    in_date = models.DateField()
    in_time = models.TimeField()
    out_date = models.DateField(blank=True)
    out_time = models.TimeField(blank=True)
    total_hour = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.employee.user.full_name} in {self.in_time}  out {self.out_time}'


@receiver(post_save, sender=EmployeeAttendanceLogModel)
def post_save(sender, instance, created, **kwargs):
    in_time = datetime.datetime.combine(instance.in_date, instance.in_time)
    out_time = datetime.datetime.combine(instance.out_date, instance.out_time)
    total_hour = out_time - in_time
    instance.total_hour = str(total_hour)
    instance.save()