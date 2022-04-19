from django.contrib import admin
from HRM_User import models

# Employee training response information
admin.site.register(models.EmployeeTrainingResponseResultModel)

# Attendance leave request
admin.site.register(models.LeaveRequestModel)
admin.site.register(models.ResignationModel)
