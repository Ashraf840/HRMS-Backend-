import base64

from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from social_core.utils import slugify

from UserApp.models import UserDepartmentModel, User
from UserApp.models import UserDepartmentModel
from django.core.validators import FileExtensionValidator, MinLengthValidator, MaxLengthValidator, EmailValidator

# Create your models here.
"""
====Admin Section====
Job post model
Filter question model
online question set model
practical question set model
"""


class JobStatusModel(models.Model):
    status = models.CharField(max_length=50, blank=False, null=False)
    statusOrder = models.IntegerField()

    def __str__(self):
        return f'{self.status}'


class JobPostModel(models.Model):
    shiftOption = (
        ('day', 'Day'),
        ('night', 'Night'),
        ('roster', 'Roster'),
    )
    jobType = (
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time'),
        ('internship', 'Internship'),
        ('freelancing', 'Freelancing'),
    )
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE, related_name='job_post_model')
    jobTitle = models.CharField(verbose_name='Job Title', max_length=100)
    lastDateOfApply = models.DateField()
    postDate = models.DateField(auto_now_add=True)
    lastUpdated = models.DateField(auto_now=True)
    level = models.CharField(max_length=255, null=True)
    shift = models.CharField(verbose_name='Shift', max_length=10, choices=shiftOption)
    location = models.CharField(verbose_name='location', max_length=255)
    department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='department_jobPost',
                                   null=True)
    vacancies = models.IntegerField()
    jobType = models.CharField(verbose_name="job type", max_length=50, choices=jobType)
    jobOverview = models.TextField(null=True)
    jobResponsibilities = models.TextField(null=True)
    jobRequirements = models.TextField(null=True)
    jobProgressStatus = models.ManyToManyField(JobStatusModel, related_name='job_progress_statusM2M')
    is_active = models.BooleanField(default=True)

    @property
    def total_applied(self):
        return self.applied_job_post_id.filter(jobPostId=self.id).count()

    # @property
    # def get_online_test_info(self):
    #     return self.job_info_online.analyticalTest

    def __str__(self):
        return f'{self.id} {self.jobTitle} {self.shift}'


# ============job apply filter questions section============

field_type = (
    (1, 'Text'),
    (2, 'Radio'),
    (3, 'Custom'),
    (4, 'Level Radio'),
)


class JobApplyFilterQuestionModel(models.Model):
    fieldType = models.CharField(max_length=50, choices=field_type)
    jobId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='filter_qus_job_info')
    question = models.CharField(max_length=255, verbose_name='filter_question')

    class Meta:
        verbose_name_plural = 'Filter Question List'

    def __str__(self):
        return f'{self.fieldType}, {self.question}'


class JobFilterQuestionRadioButtonOptionModel(models.Model):
    question = models.ForeignKey(JobApplyFilterQuestionModel, on_delete=models.CASCADE,
                                 related_name='filter_question_option_job', blank=True, null=True)
    options = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}, {self.options}'


class FilterQuestionAnswerModel(models.Model):
    """
    Filter question answer will be stored here for check and select candidate for next stage
    """

    question = models.OneToOneField(JobApplyFilterQuestionModel, on_delete=models.CASCADE,
                                    related_name='job_apply_filter_question_answer')
    answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.answer}'


class UserJobAppliedModel(models.Model):
    """
    Job application model
    """
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_user')
    jobPostId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='applied_job_post_id')
    jobProgressStatus = models.ForeignKey(JobStatusModel, on_delete=models.CASCADE,
                                          related_name='job_applied_progress_status')
    # jobProgressStatus = models.CharField(max_length=30, choices=status, blank=True)
    appliedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.jobPostId}, {self.userId}'


class FilterQuestionsResponseModelHR(models.Model):
    """
    All filter questions response will be stored in this model
    """
    questions = models.ForeignKey(JobApplyFilterQuestionModel, on_delete=models.CASCADE,
                                  related_name='filter_questions')
    response = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='response_by')
    jobPost = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='job_info')

    def __str__(self):
        return f'{self.response}'


class OnlineTestModel(models.Model):
    jobInfo = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='job_info_online')
    testName = models.CharField(max_length=256, verbose_name='Test Name', name='test_name')
    testLink = models.URLField(verbose_name='Test Link', name='test_link')

    def __str__(self):
        return f'{self.id} job ID {self.jobInfo.id}  jobInfo: {self.jobInfo} '


class PracticalTestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_user_info')
    jobInfo = models.OneToOneField(JobPostModel, on_delete=models.CASCADE, related_name='practical_job_info')
    practicalFile = models.FileField(verbose_name='Practical Test File', upload_to='users/files', blank=True)
    testLink = models.URLField(verbose_name='Test link', blank=True)
    instruction = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.jobInfo}'


"""
====Candidate section====
All candidate response will stored model section
online test response
practical test response
"""


class OnlineTestResponseModel(models.Model):
    testName = models.CharField(max_length=200)
    testMark = models.IntegerField(blank=True, verbose_name='Test Mark')
    testScnSrt = models.ImageField(upload_to='online_test/test_res/', blank=True,
                                   verbose_name='Screenshot', default='users/default.png')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='online_response_user')
    appliedJob = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
                                   related_name='job_applied_online_response')
    submittedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.testName}: {self.testMark}'


class PracticalTestResponseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_response_user')
    appliedJob = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                      related_name='job_applied_practical_response')
    practicalTestResFiles = models.FileField(upload_to='practical_test/response/',
                                             verbose_name='Practical test response', blank=True, null=True)
    practicalTestResLink = models.URLField(verbose_name='Practical test response', blank=True)
    submittedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


# for document naming
def image_file_name(instance, filename):
    return '/'.join(['images', instance.user.full_name, filename])


def content_file_name(instance, filename):
    return '/'.join(['document', instance.user.full_name + '-id_' + str(instance.user.id), filename])


class DocumentSubmissionModel(models.Model):
    """
    Candidate personal documents will stored here
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_submission_user')
    applied_job = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                       related_name='document_submission_applied_job')
    sscCertificate = models.FileField(upload_to=content_file_name)
    hscCertificate = models.FileField(upload_to=content_file_name)
    graduationCertificate = models.FileField(upload_to=content_file_name, blank=True)
    postGraduationCertificate = models.FileField(upload_to=content_file_name, blank=True)
    nidCard = models.FileField(upload_to=content_file_name, blank=True)
    userPassportImage = models.ImageField(upload_to=image_file_name, blank=True)
    passportSizePhoto = models.ImageField(upload_to=image_file_name)
    digitalSignature = models.ImageField(upload_to=image_file_name)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'pk:{self.id} id:{self.user.id},name: {self.user.full_name} Documents'


# class EmailField(models.EmailField):
#     def __init__(self, *args, **kwargs):
#         super(EmailField, self).__init__(*args, **kwargs)
#
#     def get_prep_value(self, value):
#         return str(value).lower()


class ReferenceInformationModel(models.Model):
    """
    candidate references information model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_information_user')
    applied_job = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
                                    related_name='references_submission_applied_job')
    name = models.CharField(max_length=100)
    # phoneNumber = models.PositiveIntegerField(validators=[MinLengthValidator(9), MaxLengthValidator(15)], blank=True)
    phoneNumber = models.PositiveBigIntegerField()
    relationWithReferer = models.CharField(max_length=100)
    email = models.EmailField()
    attachedFile = models.FileField(upload_to=content_file_name, blank=True, null=True)
    callRecord = models.FileField(upload_to=content_file_name, blank=True, null=True)
    slug_field = models.SlugField(max_length=255, blank=True)
    is_sent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    ref_response = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_field = slugify(base64.b64encode(str(self.name + self.email).encode('utf-8')))
        super(ReferenceInformationModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'pk: {self.pk} reference: {self.name}'


# appointment letter naming function
def appointment_file_name(instance, filename):
    return '/'.join(['OfficialDocuments', filename])


def signed_appointment_letter_name(instance, filename):
    return '/'.join(['signed_appointment_letter', instance.user.full_name, filename])


class OfficialDocumentsModel(models.Model):
    applicationId = models.ForeignKey(UserJobAppliedModel, on_delete=models.SET_NULL, related_name='application',
                                      null=True)
    appointmentLetter = models.TextField(blank=True)
    allow_applicant_access = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}, {self.allow_applicant_access}'


class SignedAppointmentLetterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='signed_appointment_letter_user')
    applicationId = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                         related_name='signed_appointment_letter_application_id')
    appointmentLetter = models.FileField(upload_to=signed_appointment_letter_name,
                                         validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return f'{self.applicationId.userId.full_name}'


class CandidateJoiningFeedbackModel(models.Model):
    applicationId = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                         related_name='candidate_joining_feedback_application_id')
    is_agree = models.BooleanField(blank=True, null=True)
    feedback = models.TextField(blank=True)
    allowed = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'{self.applicationId.userId.full_name}, {self.is_agree}'


# ============ Reference conformation data ============
class ReferenceQuestionsModel(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.question}'


class ReferenceResponseInformationView(models.Model):
    reference_id = models.ForeignKey(ReferenceInformationModel, on_delete=models.CASCADE,
                                     related_name='reference_information_reference')
    # Reference Information
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True)
    name_of_company = models.CharField(max_length=255, blank=True)
    address_of_company = models.CharField(max_length=255, blank=True)
    relation = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    res_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class ReferencesQuestionResponseModel(models.Model):
    referee = models.ForeignKey(ReferenceResponseInformationView, on_delete=models.CASCADE,
                                related_name='questions_referee_information')
    question = models.ForeignKey(ReferenceQuestionsModel, on_delete=models.CASCADE,
                                 related_name='reference_response_qus')
    response = models.TextField()


# Removing filter questions response garbage values
@receiver(pre_delete, sender=UserJobAppliedModel)
def log_deleted_question(sender, instance, **kwargs):
    filterQus = FilterQuestionsResponseModelHR.objects.filter(user=instance.userId, jobPost=instance.jobPostId).delete()


@receiver(post_save, sender=ReferenceResponseInformationView)
def ref_info_response(sender, instance, **kwargs):
    ref = instance.reference_id
    ref.ref_response = True
    ref.save()
    print(ref.ref_response)
