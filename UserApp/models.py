from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django_resized import ResizedImageField
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.shortcuts import HttpResponseRedirect
from django.core.mail import send_mail
from UserApp.utils import Util


# from HRM_Admin import models as hrm_admin_model


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
        user.email_validated = True
        user.is_employee = True
        user.is_candidate = True
        user.is_hr = True
        user.save(using=self._db)
        return user


# Custom User model
gender_options = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, verbose_name='Email', unique=True, blank=False)
    full_name = models.CharField(verbose_name='Full Name', max_length=100)

    # profile_pic = models.ImageField(upload_to='users/', default='users/default.png')
    profile_pic = ResizedImageField(upload_to='users/', blank=True, help_text='Size Recommended: 512x512',
                                    size=[512, 512], quality=100, force_format='JPEG', default='default.jpg')
    phone_number = models.CharField(max_length=30, blank=True)
    nid = models.CharField(max_length=30, null=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)

    birthDate = models.DateField(verbose_name='Date of Birth', blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Joined Date', auto_now_add=True)

    gender = models.CharField(verbose_name='Choose Gender', choices=gender_options, max_length=20, blank=True)

    is_staff = models.BooleanField(verbose_name='Staff Status', default=False, help_text='Designate if the user has '
                                                                                         'staff status')
    is_active = models.BooleanField(verbose_name='Active Status', default=True, help_text='Designate if the user has '
                                                                                          'active status')
    email_validated = models.BooleanField(verbose_name='Email Validate', default=False,
                                          help_text='Designate if the user has '
                                                    'Email Validate')
    is_superuser = models.BooleanField(verbose_name='Superuser Status', default=False, help_text='Designate if the '
                                                                                                 'user has superuser '
                                                                                                 'status')

    is_employee = models.BooleanField(verbose_name='Employee Status', default=False, help_text='Designate if the '
                                                                                               'user has Employee '
                                                                                               'status')
    is_hr = models.BooleanField(verbose_name='HR Status', default=False, help_text='Designate if the '
                                                                                   'user has HR '
                                                                                   'status')
    is_candidate = models.BooleanField(verbose_name='candidate Status', default=True, help_text='Designate if the '
                                                                                                'user has Candidate '
                                                                                                'status')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', ]

    objects = UserManager()

    def __str__(self):
        return f'{self.full_name}'


# Designation Model
class UserDesignationModel(models.Model):
    designation = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name_plural = 'Designation'

    def __str__(self):
        return self.designation


# Department Model
class UserDepartmentModel(models.Model):
    department = models.CharField(max_length=50, null=False)

    # departmentHead = models.ForeignKey(User, on_delete=models.)

    class Meta:
        verbose_name_plural = 'Department'

    def __str__(self):
        return f'{self.department}'


# User skills Model
class SkillsModel(models.Model):
    skillName = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "skills"

    def __str__(self):
        return self.skillName


# User detail information
shift_options = (
    ('Day', 'Day'),
    ('Night', 'Night'),
    ('Roster', 'Roster'),

)


# class EmployeeInfoModel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info_user')
#     # phone_number = models.IntegerField(null=True)
#     salary = models.IntegerField(null=True, blank=True)
#     designation = models.ForeignKey(UserDesignationModel, on_delete=models.CASCADE, related_name='designation_user',
#                                     null=True)
#     department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='department_user',
#                                    null=True)
#     shift = models.CharField(choices=shift_options, verbose_name='Choose Shift', max_length=20)
#     email = models.EmailField(blank=True)
#
#     class Meta:
#         verbose_name_plural = 'User_Info'
#
#     def __str__(self):
#         return f'{self.user}, Department: {self.department} Designation: {self.designation}'

# Career objective for candidate/user
class CareerObjectiveModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='career_objective_user')
    objective = models.TextField()

    def __str__(self):
        return f'{self.user.full_name}'


# user all academic information model
class EducationLevelModel(models.Model):
    """
    Education level model for User academic model foreign key value
    """
    educationLevel = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.educationLevel}'


class DegreeTitleModel(models.Model):
    """
    Degree model for User academic model foreign key value
    """
    educationLevel = models.ForeignKey(EducationLevelModel, on_delete=models.CASCADE,
                                       related_name='education_level_education')
    degree = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.degree}'


class GroupOrSubjectModel(models.Model):
    educationLevel = models.ForeignKey(EducationLevelModel, on_delete=models.CASCADE,
                                       related_name='major_group_educational_level')
    majorGroup = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.majorGroup}'


class UserAcademicInfoModel(models.Model):
    """
    User academic information model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academic_info_user')
    educationLevel = models.ForeignKey(EducationLevelModel, on_delete=models.SET_NULL, related_name='education_level',
                                       blank=True, null=True)
    degreeTitle = models.ForeignKey(DegreeTitleModel, on_delete=models.SET_NULL, related_name='degree_title',
                                    blank=True, null=True)
    instituteName = models.CharField(max_length=255, null=True)
    major = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=15, null=True, blank=True)
    duration = models.IntegerField(null=True)
    cgpa = models.DecimalField(max_digits=10, decimal_places=2)
    cgpaOutOf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)

    class Meta:
        ordering = ['year']
        verbose_name_plural = 'Academic Information'

    def __str__(self):
        return f'{self.user}, {self.major}'


def certificate_file_name(instance, filename):
    return '/'.join(['certificate', instance.user.full_name + '_id_' + str(instance.user.id), filename])


class UserCertificationsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certification_info_user')
    vendorName = models.CharField(max_length=255)
    examName = models.CharField(max_length=255)
    score = models.CharField(max_length=255)
    certificationId = models.CharField(max_length=255)
    dateOfAchievement = models.DateField(null=True, blank=True)
    dateOfExpiry = models.DateField(null=True, blank=True)
    certificateImage = models.FileField(upload_to=certificate_file_name, blank=True)

    class Meta:
        verbose_name_plural = 'Certification Information'

    @property
    def certification_expiry_date(self):
        if not self.dateOfExpiry:
            return 'No expiry date.'

    def __str__(self):
        return f'{self.user},{self.examName}'


class UserTrainingExperienceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_info_user')
    vendorName = models.CharField(max_length=255)
    topicName = models.CharField(max_length=255)
    startDate = models.DateField(blank=True)
    completeDate = models.DateField(blank=True)
    courseDuration = models.CharField(max_length=100, blank=True)
    certificateImage = models.FileField(upload_to=certificate_file_name, blank=True)

    class Meta:
        verbose_name_plural = 'Training Information'

    def __str__(self):
        return f'{self.user},{self.topicName}'


class UserWorkingExperienceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="working_experience_user")
    organizationName = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    joinDate = models.DateField(null=True)
    quitDate = models.DateField(blank=True, null=True)
    responsibility = models.TextField(blank=True, null=True)
    jobAchievement = models.TextField(blank=True, )

    class Meta:
        verbose_name_plural = 'Work Experience'

    def __str__(self):
        return f'{self.pk}, {self.user},{self.department}'


class JobPreferenceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_preference_user')
    preferredPost = models.CharField(max_length=255)
    preferredShift = models.CharField(max_length=255)
    salaryFrom = models.IntegerField()
    salaryTo = models.IntegerField()

    def __str__(self):
        return f'{self.user}'


class UserSkillsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='skills_user')
    skills = models.ManyToManyField(SkillsModel, verbose_name='user_skills')

    class Meta:
        verbose_name_plural = 'User Skills'

    def __str__(self):
        return f'{self.user}, {self.skills}'


# # for document naming
def image_file_name(instance, filename):
    return '/'.join(['images', instance.user.full_name, filename])


def content_file_name(instance, filename):
    return '/'.join(['document', instance.user.full_name + '-id_' + str(instance.user.id), filename])


"""
Change and Reset Password section model
"""


@receiver(post_save, sender=UserTrainingExperienceModel)
def post_save(sender, instance, created, **kwargs):
    if created:
        start_date = instance.startDate
        end_date = instance.completeDate
        duration = end_date - start_date
        instance.courseDuration = str(duration)
        instance.save()





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # email_plaintext_message = f'{"https://career.techforing.com/set-new-password"}'
    email_plaintext_message = 'https://career.techforing.com/auth/set-new-password/'

    email_body = 'Hi ' + \
                 f'{reset_password_token.user.full_name} Use this token to reset your password.\n' \
                 f'Visit the given link below to reset your password. \n' \
                 f'{email_plaintext_message}{reset_password_token.key} \n'

    data = {'email_body': email_body, 'to_email': reset_password_token.user.email,
            'email_subject': 'Password Reset for Techforing'}

    Util.send_email(data)
