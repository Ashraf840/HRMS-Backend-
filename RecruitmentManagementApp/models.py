from django.db import models
from UserApp.models import UserDepartmentModel, User
from QuizApp.models import JobApplyFilterQuestionModel
from UserApp.models import UserDepartmentModel

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

    # is_completed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.status}'


class JobPostModel(models.Model):
    shiftOption = (
        ('day', 'Day'),
        ('night', 'Night'),
    )
    jobType = (
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time'),
        ('internship', 'Internship'),
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
    jobDescription = models.TextField(null=True)
    # uploadCV = models.FileField(upload_to='user/')
    filterQuestions = models.ManyToManyField(JobApplyFilterQuestionModel, related_name='filter_question_list')
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


class UserJobAppliedModel(models.Model):
    """
    Job application model
    """
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_user')
    jobPostId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='applied_job_post_id')
    jobProgressStatus = models.ForeignKey(JobStatusModel, on_delete=models.CASCADE,
                                          related_name='job_applied_progress_status')
    # jobProgressStatus = models.CharField(max_length=30, choices=status, blank=True)
    appliedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.jobPostId}, {self.userId}'


class FilterQuestionsResponseModelHR(models.Model):
    """
    All filter questions response will be stored in this model
    """
    questions = models.ForeignKey(JobApplyFilterQuestionModel, on_delete=models.CASCADE,
                                  related_name='filter_questions')
    response = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='response_by')
    jobPost = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='job_info')

    # appliedJob = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
    #                                related_name='filter_question_job_application')

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
    practicalFile = models.FileField(verbose_name='Practical Test File', upload_to='users/files')
    testLink = models.URLField(verbose_name='Test link', blank=True)

    def __str__(self):
        return f'{self.jobInfo}'


"""
====Candidate section====
All candidate response will stored model section
online test response
practical test response
"""


#     order= models.T

# status = (
#         ('new', 'new'),
#         ('online', 'online'),
#         ('under_review', 'under_review'),
#         ('practical', 'practical'),
#         ('test_under_review', 'test_under_review'),
#         ('interview', 'interview'),
#         ('document', 'document'),
#         ('reference', 'reference'),
#         ('verification', 'verification'),
#         ('appointed', 'appointed'),
#         ('rejected', 'rejected')
#
#     )


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
                                             verbose_name='Practical test response', blank=True)
    practicalTestResLink = models.URLField(verbose_name='Practical test response', blank=True)
    submittedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


# class PracticalTestEvaluationModel(models.Model):
#     choice = (
#         ('A', 'A'),
#         ('B', 'B'),
#         ('C', 'C'),
#         ('C', 'Fail'),
#     )
#     practicalTest = models.OneToOneField(PracticalTestResponseModel, on_delete=models.CASCADE,
#                                          related_name='practical_test_evaluation_practical_res')
#     grade = models.CharField(max_length=10,choices=choice)


# for document naming
def image_file_name(instance, filename):
    return '/'.join(['images', instance.user.full_name, filename])


def content_file_name(instance, filename):
    return '/'.join(['document', instance.user.full_name + '-id_' + str(instance.user.id), filename])


class DocumentSubmissionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_submission_user')
    applied_job = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                       related_name='document_submission_applied_job')
    sscCertificate = models.FileField(upload_to=content_file_name, blank=True)
    hscCertificate = models.FileField(upload_to=content_file_name, blank=True)
    graduationCertificate = models.FileField(upload_to=content_file_name, blank=True)
    postGraduationCertificate = models.FileField(upload_to=content_file_name, blank=True)
    nidCard = models.FileField(upload_to=content_file_name, blank=True)
    userPassportImage = models.ImageField(upload_to=image_file_name, blank=True)
    passportSizePhoto = models.ImageField(upload_to=image_file_name, blank=True)
    digitalSignature = models.ImageField(upload_to=image_file_name, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'pk:{self.id} id:{self.user.id},name: {self.user.full_name} Documents'


class ReferenceInformationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_information_user')
    applied_job = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
                                    related_name='references_submission_applied_job')
    name = models.CharField(max_length=100)
    phoneNumber = models.IntegerField()
    relationWithReferer = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    attachedFile = models.FileField(upload_to=content_file_name, blank=True, null=True)
    callRecord = models.FileField(upload_to=content_file_name, blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'pk: {self.pk} reference: {self.name}'


def appointment_file_name(instance, filename):
    return '/'.join(['OfficialDocuments', filename])


# class ReferenceAuthorConfirmationResModel(models.Model):
#


class OfficialDocumentsModel(models.Model):
    applicationId = models.ForeignKey(UserJobAppliedModel, on_delete=models.SET_NULL, related_name='application', null=True)
    appointmentLetter = models.TextField()

    def __str__(self):
        return f'{self.id} {self.applicationId.userId.full_name}'
