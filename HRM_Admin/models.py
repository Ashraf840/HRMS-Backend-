from django.db import models
from UserApp import models as userModel

# Create your models here.


project_status = (
    ('new', 'new'),
    ('on_progress', 'On Progress'),
    ('finished', 'Finished'),
)


class EmployeeInformationModel(models.Model):
    """
    Employee information model, emp salary, personal email, dpet, ect
    """
    user = models.OneToOneField(userModel.User, on_delete=models.CASCADE, related_name='employee_user_info')
    personal_email = models.EmailField(unique=True, blank=True)
    emp_department = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE, blank=True,
                                       related_name='employee_department')
    designation = models.ForeignKey(userModel.UserDesignationModel, on_delete=models.CASCADE, blank=True,
                                    related_name='employee_designation')
    joining_date = models.DateField(blank=True)

    def __str__(self):
        return f'{self.user.full_name}, {self.emp_department.department}'


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
    project_title = models.CharField(max_length=255)
    project_manager = models.ForeignKey(EmployeeInformationModel, on_delete=models.SET_NULL, null=True,
                                        related_name='project_manager_employee')
    project_description = models.TextField(blank=True)
    project_status = models.CharField(max_length=50, choices=project_status, blank=True)
    project_assignTo = models.ManyToManyField(EmployeeInformationModel, related_name='project_assign_to_employee')
    project_deadline = models.DateField(blank=True)

    def __str__(self):
        return f'P{self.id}, {self.project_title}'


class EmployeeEmergencyContactModel(models.Model):
    employee = models.ForeignKey(EmployeeInformationModel, on_delete=models.CASCADE,
                                 related_name='employee_emergency_contact_info')
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    phoneNo = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.employee.user.full_name}, {self.relation}'


class EmployeeBankInfoModel(models.Model):
    employee = models.OneToOneField(EmployeeInformationModel, on_delete=models.CASCADE,
                                    related_name='employee_bank_info')
    account_no = models.CharField(max_length=100)
    account_name = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.employee.user.full_name}, {self.account_no}'
