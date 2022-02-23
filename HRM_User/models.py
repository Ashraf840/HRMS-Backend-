from django.db import models
from UserApp import models as user_model
from HRM_Admin import models as hrm_admin_model


# Create your models here.

class EmployeeTrainingResponseResultModel(models.Model):
    employee = models.ForeignKey(user_model.User, on_delete=models.CASCADE, related_name='employee_test_result_user')
    test = models.ForeignKey(hrm_admin_model.TrainingModel, on_delete=models.CASCADE, related_name='employee_training_response')
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



#  ================= Employee
