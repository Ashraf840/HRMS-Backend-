from django.contrib import admin
from HRM_controller import models

# Register your models here.
# Survey Section
admin.site.register(models.SurveyAnswerSheetModel)
admin.site.register(models.SurveyQuestionModel)
admin.site.register(models.SurveyUserResponseModel)
# Colleague Evaluation Section
admin.site.register(models.EmployeeCriteriaModel)
admin.site.register(models.EmployeeEvaluationModel)
# Announcement, Notice and Complain
admin.site.register(models.AnnouncementModel)
admin.site.register(models.NoticeModel)
admin.site.register(models.ComplainModel)
# Attendance Holidays, in/out logs Section
admin.site.register(models.HolidayModel)
admin.site.register(models.ShiftTimeModel)
admin.site.register(models.AttendanceShiftTimeModel)
admin.site.register(models.AttendanceEmployeeRelModel)
admin.site.register(models.AttendanceEmployeeShiftRelModel)
admin.site.register(models.EmployeeAttendanceLogModel)
# test
admin.site.register(models.TestModel)
