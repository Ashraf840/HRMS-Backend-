from django.contrib import admin
from HRM_Admin import models as hrm_admin

# Employee section
admin.site.register(hrm_admin.EmployeeInformationModel)
admin.site.register(hrm_admin.EmployeeSalaryModel)
admin.site.register(hrm_admin.EmployeeBankInfoModel)
admin.site.register(hrm_admin.EmployeeEmergencyContactModel)
# project information
admin.site.register(hrm_admin.ProjectInformationModel)
# Module permission
admin.site.register(hrm_admin.ModulePermissionModel)
# Training information
admin.site.register(hrm_admin.TrainingModel)
admin.site.register(hrm_admin.PaidInvoicesModel)
admin.site.register(hrm_admin.WarrentyListModel)
admin.site.register(hrm_admin.EmployeeSalarySheetModel)

