from django.contrib import admin
from UserApp.models import User, UserDesignationModel, UserDepartmentModel, UserInfoModel
from . import models
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AdminUser(UserAdmin):
    ordering = ('-date_joined',)
    search_fields = ('email', 'full_name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'gender',)
    list_display = ('id','email', 'full_name', 'gender', 'date_joined', 'is_active','is_hr')
    fieldsets = (
        ('Login Info', {'fields': ('email', 'password')}),
        ('User Information',
         {'fields': ('full_name', 'gender', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_employee','is_candidate')}),

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
admin.site.register(UserInfoModel)
admin.site.register(UserDesignationModel)
admin.site.register(UserDepartmentModel)
admin.site.register(models.UserAcademicInfoModel)
admin.site.register(models.UserTrainingExperienceModel)
admin.site.register(models.UserCertificationsModel)
admin.site.register(models.JobPreferenceModel)
admin.site.register(models.UserWorkingExperienceModel)


# admin.site.register(JobPostModel)
