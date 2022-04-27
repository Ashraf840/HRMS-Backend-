from django.db import models
from UserApp import models as user_model
from HRM_Admin import models as hrm_admin_model


# Create your models here.

class EmployeeTrainingResponseResultModel(models.Model):
    employee = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name='employee_test_result_user')
    test = models.ForeignKey(hrm_admin_model.TrainingModel, on_delete=models.CASCADE,
                             related_name='employee_training_response')
    test_mark = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.id} - {self.employee}, {self.test_mark}'


# class EmployeeAttendanceAccessModel(models.Model):
#     employee = models.OneToOneField(user_model.User, on_delete=models.CASCADE, related_name='attendance_access_user')
#     employee_attendance_id = models.CharField(max_length=10, unique=True)
#
#
# class EmployeeAttendanceModel(models.Model):
#     employee = models.ForeignKey(EmployeeAttendanceAccessModel, on_delete=models.CASCADE, related_name='attendance_attendance_access')
#     date = models.DateField()
#     in_time = models.TimeField()
#     out_time = models.TimeField()


#  ================= Employee Leave Request Model =================
leave_type = (
    ('casual', 'Casual Leave'),
    ('medical', 'Medical Leave'),
    ('maternity', 'Maternity Leave'),
    ('wedding', 'Wedding Leave'),
    ('sick', 'Sick Leave'),
)
leave_status = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled')
)


class LeaveRequestModel(models.Model):
    employee = models.ForeignKey(hrm_admin_model.EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='leave_request_employee')
    leave_type = models.CharField(max_length=255, choices=leave_type)
    leave_from = models.DateField()
    leave_to = models.DateField()
    no_of_days = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True,choices=leave_status, default='pending')
    reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(hrm_admin_model.EmployeeInformationModel, on_delete=models.SET_NULL, blank=True,
                                    null=True)

    def __str__(self):
        return f'{self.id} - {self.employee}, {self.leave_type}'

#  ================= Employee Resignation Request Model =================

# resignation_chooice=[('pending','Pending'),
#                      ('accepted','Accepted')]
# class ResignationModel(models.Model):
#     employee=models.OneToOneField(hrm_admin_model.EmployeeInformationModel, on_delete=models.CASCADE, related_name='resignation_employee')
#     reason = models.TextField()
#     resignationDate = models.DateField(auto_now_add=True)
#     noticeDate = models.DateField()
#     resignationstaus=models.CharField(max_length=50,choices=resignation_chooice, default='pending')
#     resignatioAcceptDate=models.DateField(null=True,blank=True)

#     def __str__(self):
#         return f'{self.id},{self.employee}, {self.resignationDate}'

# question_choices=[
#     ('text','Text'),
#     ('bool','Bool'),
# ]
# class ExitInterviewQuestionModel(models.Model):
#     question = models.TextField()
#     question_type = models.CharField(max_length=50,choices=question_choices, default='text')
#     def __str__(self):
#         return f'{self.id} - {self.question}'

# class ExitInterviewAnswerModel(models.Model):
#     resignation = models.ForeignKey(ResignationModel, on_delete=models.CASCADE,blank=False, null=True,
#                                  related_name='answer_employee')
#     question = models.ForeignKey(ExitInterviewQuestionModel, on_delete=models.CASCADE, blank=False, null=True,
#                                  related_name='answer_question')
#     answer = models.TextField(blank=True)

#     def __str__(self):
#         return f'{self.id} - {self.resignation}, {self.question}'


