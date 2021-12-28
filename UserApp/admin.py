from django.contrib import admin
from UserApp.models import User, UserDesignationModel, UserDepartmentModel, EmployeeInfoModel
from . import models
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AdminUser(UserAdmin):
    ordering = ('-date_joined',)
    search_fields = ('email', 'full_name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser','email_validated', 'gender',)
    list_display = ('id', 'email', 'full_name', 'profile_pic', 'phone_number', 'nationality', \
                    'location', 'birthDate', 'gender', 'date_joined', 'is_active', 'is_hr','email_validated',)
    fieldsets = (
        ('Login Info', {'fields': ('email', 'password')}),
        ('User Information',
         {'fields': ('full_name', 'gender', 'profile_pic', 'phone_number', 'nationality', 'location', 'birthDate')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_employee', \
                                    'is_candidate', 'is_hr','email_validated')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )


# class UserInfo(UserDesignationModel):
#     list_display = ('user', 'phone_number')


admin.site.register(User, AdminUser)
admin.site.register(EmployeeInfoModel)
admin.site.register(UserDesignationModel)
admin.site.register(UserDepartmentModel)
admin.site.register(models.UserAcademicInfoModel)
admin.site.register(models.UserTrainingExperienceModel)
admin.site.register(models.UserCertificationsModel)
admin.site.register(models.JobPreferenceModel)
admin.site.register(models.UserWorkingExperienceModel)
admin.site.register(models.SkillsModel)
admin.site.register(models.UserSkillsModel)
# admin.site.register(models.DocumentSubmissionModel)
# admin.site.register(models.ReferenceInformationModel)


# admin.site.register(JobPostModel)
