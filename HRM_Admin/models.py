from django.db import models
from UserApp import models as userModel

# Create your models here.


projectStatus = (
    ('new', 'new'),
    ('on_progress', 'On Progress'),
    ('finished', 'Finished'),
)


class EmployeeInformationModel(models.Model):
    """
    Employee information model, emp salary, personal email, dpet, ect
    """
    user = models.OneToOneField(userModel.User, on_delete=models.CASCADE, related_name='employee_user_info')
    personalEmail = models.EmailField(unique=True, blank=True)
    empDepartment = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE, blank=True,
                                      related_name='employee_department')
    designation = models.ForeignKey(userModel.UserDesignationModel, on_delete=models.CASCADE, blank=True,
                                    related_name='employee_designation')
    joiningDate = models.DateField(blank=True)

    def __str__(self):
        return f'{self.user.full_name}, {self.empDepartment.department}'


class EmployeeSalaryModel(models.Model):
    """
    employee salary will store here
    """
    employee = models.ForeignKey(EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='employee_salary_employee')
    salary = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.id} - {self.employee.user.full_name}, {self.salary}'


class ProjectInformationModel(models.Model):
    """
    Project Description and assigned manager and employee, deadline
    """
    projectTitle = models.CharField(max_length=255)
    projectManager = models.ForeignKey(EmployeeInformationModel, on_delete=models.SET_NULL, null=True,
                                       related_name='project_manager_employee')
    projectDescription = models.TextField(blank=True)
    projectStatus = models.CharField(max_length=50, choices=projectStatus, blank=True)
    projectAssignTo = models.ManyToManyField(EmployeeInformationModel, related_name='project_assign_to_employee')
    projectDeadline = models.DateField(blank=True)

    def __str__(self):
        return f'P{self.id}, {self.projectTitle}'


class EmployeeEmergencyContactModel(models.Model):
    employee = models.ForeignKey(EmployeeInformationModel, on_delete=models.CASCADE, related_name='employee_emergency_contact_info')
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    phoneNo = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.employee.user.full_name}, {self.relation}'


class EmployeeBankInfoModel(models.Model):
    employee = models.OneToOneField(EmployeeInformationModel, on_delete=models.CASCADE, related_name='employee_bank_info')
    accountNo = models.CharField(max_length=100)
    accountName = models.CharField(max_length=255, blank=True)
    bankName = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.employee.user.full_name}, {self.accountNo}'

