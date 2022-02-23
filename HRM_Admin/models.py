from django.db import models
from UserApp import models as userModel
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

# Create your models here.

project_status = (
    ('new', 'new'),
    ('on_progress', 'On Progress'),
    ('finished', 'Finished'),
)

employee_shift = (
    ('day', 'Day'),
    ('night', 'Night'),
    ('roster', 'Roster'),
)


class EmployeeInformationModel(models.Model):
    """
    Employee information model, emp salary, personal email, dpet, ect
    """
    user = models.OneToOneField(userModel.User, on_delete=models.CASCADE, related_name='employee_user_info')
    # official_email = models.EmailField(unique=True, blank=True)
    emp_department = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE, blank=True,
                                       related_name='employee_department')
    designation = models.ForeignKey(userModel.UserDesignationModel, on_delete=models.CASCADE, blank=True,
                                    related_name='employee_designation')
    shift = models.CharField(max_length=200, choices=employee_shift)
    joining_date = models.DateField(blank=True)
    employee_is_permanent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.full_name}, {self.emp_department.department} - {self.designation.designation}'


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


class ModulePermissionModel(models.Model):
    employee = models.OneToOneField(EmployeeInformationModel, on_delete=models.CASCADE,
                                    related_name='module_permission_employee')
    is_superuser = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)
    is_gm = models.BooleanField(default=False)
    is_hrm = models.BooleanField(default=False)
    is_hre = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    is_pm = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.employee}'


class TrainingModel(models.Model):
    department = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE,
                                   related_name='employee_training_department', blank=True, null=True)
    passing_mark = models.PositiveIntegerField()
    training_name = models.CharField(max_length=255)
    training_link = models.URLField()

    def __str__(self):
        return f'{self.training_name}'


@receiver(post_save, sender=EmployeeInformationModel)
def create_employee_module_permission(sender, instance, created, **kwargs):
    """
    Create permission access while assign employee info
    """
    if created:
        instance.user.is_employee = True
        instance.user.is_candidate = False
        instance.user.save()
        data = ModulePermissionModel.objects.create(employee=instance)
        return data

# @receiver(pre_delete, sender=EmployeeInformationModel)
# def employee_deleted(sender, instance, using, **kwargs):
#     instance.user.is_employee = False
#     instance.user.is_hr = False
#     instance.user.is_active = False
#     instance.user.save()
