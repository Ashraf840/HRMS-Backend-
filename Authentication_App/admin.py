from django.contrib import admin
from Authentication_App.models import User, UserDesignationModel, UserDepartmentModel, UserInfoModel
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class AdminUser(UserAdmin):
    ordering = ('-date_joined',)
    search_fields = ('email', 'full_name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'gender',)
    list_display = ('email', 'full_name', 'gender', 'date_joined', 'is_active')
    fieldsets = (
        ('Login Info', {'fields': ('email', 'password')}),
        ('User Information',
         {'fields': ('full_name', 'gender', 'profile_pic', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_hr', 'is_employee','is_candidate')}),

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
