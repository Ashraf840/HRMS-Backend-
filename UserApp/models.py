from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django_resized import ResizedImageField


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
        user.save(using=self._db)
        return user


# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, verbose_name='Email', unique=True, blank=False)
    full_name = models.CharField(verbose_name='Full Name', max_length=100)

    # profile_pic = models.ImageField(upload_to='users/', default='users/default.png')
    profile_pic = ResizedImageField(upload_to='users/', blank=False, help_text='Size Recommended: 512x512',
                                    size=[512, 512], quality=100, force_format='JPEG')
    phone_number = models.CharField(max_length=30, blank=True)
    nid = models.CharField(max_length=30, null=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)

    birthDate = models.DateField(verbose_name='Date of Birth', blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Joined Date', auto_now_add=True)
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
        return f'{self.id}'


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
    deptManager = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Department'

    def __str__(self):
        return f'{self.department}, {self.deptManager}'


# User skills Model
class SkillsModel(models.Model):
    skillName = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "User skills"

    def __str__(self):
        return self.skillName


# User detail information
class UserInfoModel(models.Model):
    shift_options = (
        ('Day', 'Day'),
        ('Night', 'Night'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info_user')
    # phone_number = models.IntegerField(null=True)
    salary = models.IntegerField(null=True)
    designation = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='designation_user')
    department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='department_user')
    shift = models.CharField(choices=shift_options, verbose_name='Choose Shift', max_length=20)
    userSkills = models.ManyToManyField(SkillsModel, related_name="user_skills")

    class Meta:
        verbose_name_plural = 'User_Info'

    def __str__(self):
        return f'{self.user}, Department: {self.department} Designation: {self.designation}'


# user all academic information model
class UserAcademicInfoModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academic_info_user')
    educationLevel = models.CharField(max_length=255, null=True)
    degreeTitle = models.CharField(max_length=255, null=True)
    instituteName = models.CharField(max_length=255, null=True)
    major = models.CharField(max_length=255, null=True)
    year = models.DateField(null=True)
    duration = models.IntegerField(null=True)
    cgpa = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Academic Information'

    def __str__(self):
        return f'{self.user}, {self.major}'


class UserCertificationsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certification_info_user')
    vendorName = models.CharField(max_length=255)
    examName = models.CharField(max_length=255)
    score = models.CharField(max_length=255)
    certificationId = models.CharField(max_length=255)
    dateOfAchievement = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'Certification Information'

    def __str__(self):
        return f'{self.user},{self.examName}'


class UserTrainingExperienceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_info_user')
    vendorName = models.CharField(max_length=255)
    topicName = models.CharField(max_length=255)
    startDate = models.DateField()
    completeDate = models.DateField()

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
    quitDate = models.DateField(null=True)
    responsibility = models.CharField(max_length=255, null=True)

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


# for document naming
def image_file_name(instance, filename):
    return '/'.join(['images', instance.user.full_name, filename])


def content_file_name(instance, filename):
    return '/'.join(['document', instance.user.full_name + '-id_' + str(instance.user.id), filename])


class DocumentSubmissionModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='document_submission_user')
    sscCertificate = models.FileField(upload_to=content_file_name)
    hscCertificate = models.FileField(upload_to=content_file_name)
    graduationCertificate = models.FileField(upload_to=content_file_name)
    postGraduationCertificate = models.FileField(upload_to=content_file_name, blank=True)
    nidCard = models.FileField(upload_to=content_file_name, blank=True)
    userPassportImage = models.ImageField(upload_to=image_file_name)

    def __str__(self):
        return f'pk:{self.id} id:{self.user.id},name: {self.user.full_name} Documents'


class ReferenceInformationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_information_user')
    name = models.CharField(max_length=100)
    phoneNumber = models.IntegerField()
    relationWithReferer = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    attachedFile = models.FileField(upload_to=content_file_name, blank=True, null=True)

    def __str__(self):
        return f'pk: {self.pk} reference: {self.name}'

# # LogOut -> BlackList API
# class BlackListedToken(models.Model):
#     token = models.CharField(max_length=500)
#     user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ("token", "user")
