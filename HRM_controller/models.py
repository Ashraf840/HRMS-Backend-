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

now = datetime.datetime.now()


class SurveyQuestionModel(models.Model):
    question = models.CharField(max_length=255)
    # answers = models.ManyToManyField(SurveyAnswerSheetModel, related_name='questions_answers')
    department= models.ManyToManyField(user_model.UserDepartmentModel, related_name='question_department')
    created_date=models.DateField(auto_now_add=True)
    # month=models.IntegerField(default=datetime.datetime.today().month)
    # year=models.IntegerField(default=datetime.datetime.today().year)
    month=models.CharField(max_length=255,default=now.strftime("%B"))
    year=models.CharField(max_length=255,default=now.strftime("%Y"))
    
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
    title=models.CharField(max_length=255)
    department = models.ManyToManyField(user_model.UserDepartmentModel, related_name='announcement_department')
    message = models.TextField()


class NoticeModel(models.Model):
    department = models.ManyToManyField(user_model.UserDepartmentModel, related_name='notice_department')
    title = models.CharField(max_length=255)
    message = models.TextField()
    # attachment = models.FileField()
    employee=models.ManyToManyField(user_model.User,related_name='notice_employee')


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
    month=models.CharField(max_length=255,default=now.strftime("%B"))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.holiday_name} - {self.holiday_date.strftime("%d-%B-%Y")} - {self.is_active}'


# ==================Attendance Section ==================
# Attendance Shift, relation model
class ShiftTimeModel(models.Model):
    time_slot = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.time_slot} - ({self.start_time}-{self.end_time})'


class AttendanceShiftTimeModel(models.Model):
    shift_name = models.CharField(max_length=255)
    shift_time = models.ForeignKey(ShiftTimeModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.shift_name}'


class AttendanceEmployeeRelModel(models.Model):
    employee = models.OneToOneField(hrm_models.EmployeeInformationModel, on_delete=models.SET_NULL,
                                    related_name='attendance_employee_relation', blank=True, null=True)
    registration_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.registration_id}, {self.employee}'


class AttendanceEmployeeShiftRelModel(models.Model):
    employee_relation = models.OneToOneField(AttendanceEmployeeRelModel, on_delete=models.CASCADE,
                                             related_name='attendance_employee_relation')
    shift = models.ForeignKey(AttendanceShiftTimeModel, on_delete=models.CASCADE,
                              related_name='attendance_employee_shift')

    def __str__(self):
        return f'{self.employee_relation} - {self.shift}'


class EmployeeAttendanceLogModel(models.Model):
    employee = models.ForeignKey(AttendanceEmployeeRelModel, on_delete=models.CASCADE,
                                 related_name='employee_attendance_log')
    in_date = models.DateField()
    in_time = models.TimeField()
    out_date = models.DateField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)
    total_hour = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.employee.registration_id} in {self.in_time}  out {self.out_time}'



@receiver(post_save, sender=EmployeeAttendanceLogModel)
def post_save(sender, instance, created, **kwargs):
    try:
        in_time = datetime.datetime.combine(instance.in_date, instance.in_time)
        out_time = datetime.datetime.combine(instance.out_date, instance.out_time)
        total_hour = out_time - in_time
        instance.total_hour = str(total_hour)
        instance.save()
    except:
        pass

'''
Promotion Section 
'''
#make a model for promotion employee from prvious designation to new designations
class EmployeePromotionModel(models.Model):
    employee = models.OneToOneField(hrm_models.EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='promotion_employee')
    promotion_from= models.CharField(max_length=255)
    promotion_to = models.ForeignKey(user_model.UserDesignationModel, on_delete=models.CASCADE, related_name='promotion_to')
    promotion_date = models.DateField()

    def __str__(self):
        return f'{self.employee} - {self.promotion_to} - {self.promotion_date}'

'''
Termination Section
'''

class TerminationTitleModel(models.Model):
    termination_title= models.CharField(max_length=255)

    def __str__(self):
        return f'{self.termination_title}'
    
#make a termination model for employee
class EmployeeTerminationModel(models.Model):
    employee = models.ForeignKey(hrm_models.EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='termination_employee')
    termination_title = models.ForeignKey(TerminationTitleModel, on_delete=models.CASCADE)
    termination_date = models.DateField()
    termination_reason = models.TextField()
    notice_date= models.DateField()
    exit_interview=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.employee} - {self.termination_title} - {self.termination_date}'