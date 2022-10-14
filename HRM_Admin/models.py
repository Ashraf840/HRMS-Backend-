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

uploaded_person=(
    ('hr', 'HR'),
    ('gm', 'GM'),
    ('ceo', 'CEO'),
    ('pm', 'PM'),
)


purchase_type = (
    ('bank', 'Bank'),
    ('cash', 'Cash'),
)

#Model for Employee Information
class EmployeeInformationModel(models.Model):
    """
    Employee information model, emp salary, personal email, dept, ect
    """
    user = models.OneToOneField(userModel.User, on_delete=models.CASCADE, related_name='employee_user_info')
    personal_email = models.EmailField(blank=True, null=True)
    emp_department = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE, blank=True,
                                       related_name='employee_department')
    designation = models.ForeignKey(userModel.UserDesignationModel, on_delete=models.CASCADE, blank=True,
                                    related_name='employee_designation')
    shift = models.CharField(max_length=200, choices=employee_shift)
    joining_date = models.DateField(blank=True)

    employee_is_permanent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.user.full_name}, {self.emp_department.department} - {self.designation.designation}'

# Model for PaidInvoice
class PaidInvoicesModel(models.Model):
    invoice_name=models.FileField(upload_to='paid_invoices',max_length=100)
    Created_date=models.DateField()
    item_name=models.CharField(max_length=100)
    quantity=models.IntegerField()
    uploaded_by=models.CharField(max_length=100,choices=uploaded_person)
    amount=models.CharField(max_length=100)
    month=models.CharField(max_length=100,default="")
    year=models.CharField(max_length=100,default="")
    purchase_type=models.CharField(max_length=200, choices=purchase_type)
    expanse_type=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.item_name}, {self.amount}'




# Model for Warrenty
class WarrentyListModel(models.Model):
    # invoice_name=models.FileField(upload_to='paid_invoices',max_length=100)
    item_name=models.CharField(max_length=100)
    created_date=models.DateField()
    warranty_end=models.DateField()
    warranty_file=models.FileField(upload_to="warranty_items",max_length=100)
    uploaded_by=models.CharField(max_length=100,choices=uploaded_person)
    item_category=models.CharField(max_length=200)
    expense_type=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.item_name}'


# # Employee Salary sheet :

class EmployeeSalarySheetModel(models.Model):
    employee=models.ForeignKey(userModel.User,on_delete=models.CASCADE,related_name='employee_sheet')
    # shift=models.ForeignKey(EmployeeInformationModel,on_delete=models.CASCADE,related_name='employee_shift_sheet',default='')
    shift=models.CharField(max_length=100,choices=employee_shift)
    # full_name=models.ForeignKey(userModel.User,on_delete=models.CASCADE,related_name='employee_full_name')
    emp_department = models.ForeignKey(userModel.UserDepartmentModel, on_delete=models.CASCADE,
                                       related_name='employee_department_sheet')
    designation = models.ForeignKey(userModel.UserDesignationModel, on_delete=models.CASCADE,
                                    related_name='employee_designation_sheet')
    #emp_salary=models.ForeignKey(hrmAdminModel.EmployeeSalaryModel,on_delete=models.CASCADE,related_name='employee_salary')
    salary=models.CharField(max_length=100)
    month=models.CharField(max_length=100)
    paid_in=models.DateField()
    absent=models.IntegerField(default=0)
    total_late_hours=models.IntegerField(default=0)
    status=models.CharField(max_length=100)
    # signature=models.ForeignKey(userModel.User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee} {self.designation} {self.month}" 



class NewSalarySheetModel(models.Model):
    employee=models.ForeignKey(EmployeeInformationModel,on_delete=models.CASCADE,related_name='new_employee_sheet')
    amount=models.IntegerField()
    paid_in=models.DateField()
    # shift=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.employee} {self.paid_in}" 


class EmployeeSalaryModel(models.Model):
    """
    employee salary will store here
    """
    employee = models.OneToOneField(EmployeeInformationModel, on_delete=models.CASCADE,
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
        return f'{self.id} - {self.employee.user.full_name}, {self.relation}'


class EmployeeBankInfoModel(models.Model):
    employee = models.OneToOneField(EmployeeInformationModel, on_delete=models.CASCADE,
                                    related_name='employee_bank_info')
    account_no = models.CharField(max_length=100)
    account_name = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    bank_branch = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.id} - {self.employee.user.full_name}, {self.account_no}'


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
    training_link = models.URLField(blank=True)
    assign_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.training_name}'


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
