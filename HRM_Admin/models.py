from django.db import models
from UserApp import models as userModel


# Create your models here.

class EmployeeInformationModel(models.Model):
    employee = models.OneToOneField(userModel.User, on_delete=models.CASCADE, related_name='employee_user_info')
    personalEmail = models.EmailField(unique=True, blank=True)
    empDepartment = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE, related_name='employee_department')
    designation = models.ForeignKey(userModel.UserDesignationModel, on_delete=models.CASCADE, related_name='employee_designation')
    joiningDate = models.DateField(blank=True)



