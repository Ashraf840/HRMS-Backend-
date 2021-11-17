from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):

        if not email:
            raise ValueError('Email should not be empty')
        if not full_name:
            raise ValueError('Name should not be empty')
        if not password:
            raise ValueError('Password should not be empty')

        user = self.model(
            email=self.normalize_email(email=email),
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email=email, full_name=full_name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

# user authentication model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, verbose_name='Email', unique=True, blank=False)
    full_name = models.CharField(verbose_name='Full Name', max_length=100)

    profile_pic = models.ImageField(upload_to='users/', default='users/default.jpg')
    birth_date = models.DateField(verbose_name='Birth Date', blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    gender_options = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    gender = models.CharField(verbose_name='Choose Gender', choices=gender_options, max_length=20)

    is_staff = models.BooleanField(verbose_name='Staff Status', default=False, help_text='Designate if the user has '
                                                                                         'staff status')
    is_active = models.BooleanField(verbose_name='Active Status', default=True, help_text='Designate if the user has '
                                                                                          'active status')
    is_superuser = models.BooleanField(verbose_name='Superuser Status', default=False, help_text='Designate if the '
                                                                                                 'user has superuser '
                                                                                                 'status')
    is_hr = models.BooleanField(verbose_name='Hr Status', default=False, help_text='Designate if the '
                                                                                   'user has Hr '
                                                                                   'status')
    is_employee = models.BooleanField(verbose_name='Employee Status', default=False, help_text='Designate if the '
                                                                                               'user has Employee '
                                                                                               'status')
    is_candidate = models.BooleanField(verbose_name='candidate Status', default=False, help_text='Designate if the '
                                                                                                 'user has Candidate '
                                                                                                 'status')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', ]

    objects = UserManager()

    def __str__(self):
        return self.full_name


class UserDesignationModel(models.Model):
    designation = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name_plural = 'Designation'

    def __str__(self):
        return self.designation


class UserDepartmentModel(models.Model):
    department = models.CharField(max_length=50, null=False)
    deptManager = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Department'

    def __str__(self):
        return f'{self.department}, {self.deptManager}'


class UserInfoModel(models.Model):
    shift_options = (
        ('Day', 'Day'),
        ('Night', 'Night'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permission_user')
    phone_number = models.IntegerField(null=True)
    designation = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='user_designation')
    department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='user_department')
    salary = models.IntegerField(null=True)
    shift = models.CharField(verbose_name='Choose Shift', choices=shift_options, max_length=20)

    class Meta:
        verbose_name_plural = 'User_Info'

    def __str__(self):
        return f'{self.user}, Department: {self.department} Designation: {self.designation}'
