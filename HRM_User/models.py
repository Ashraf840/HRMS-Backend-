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
        return f'{self.employee}, {self.test_mark}'


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
    'pending', 'Pending',
    'approved', 'Approved',
    'rejected', 'Rejected',
)


class LeaveRequestModel(models.Model):
    employee = models.ForeignKey(hrm_admin_model.EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='leave_request_employee')
    leave_type = models.CharField(max_length=255, choices=leave_type)
    leave_from = models.DateField()
    leave_to = models.DateField()
    no_of_days = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)
    reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(hrm_admin_model.EmployeeInformationModel, on_delete=models.SET_NULL, blank=True,
                                    null=True)

    def __str__(self):
        return f'{self.employee}- {self.leave_type}'



