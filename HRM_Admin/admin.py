from django.contrib import admin
from HRM_Admin import models as hrm_admin

# Register your models here.

admin.site.register(hrm_admin.EmployeeInformationModel)
admin.site.register(hrm_admin.EmployeeSalaryModel)
admin.site.register(hrm_admin.ProjectInformationModel)
admin.site.register(hrm_admin.EmployeeBankInfoModel)
admin.site.register(hrm_admin.EmployeeEmergencyContactModel)
admin.site.register(hrm_admin.ModulePermissionModel)

