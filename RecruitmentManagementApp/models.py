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


class JobPostModel(models.Model):

    shiftOption = (
        ('day', 'Day'),
        ('night', 'Night'),
    )
    jobType = (
        ('pert_time', 'Pert Time'),
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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.jobTitle} {self.shift}'


class FilterQuestionsResponseModelHR(models.Model):
    questions = models.ForeignKey(JobApplyFilterQuestionModel, on_delete=models.CASCADE,
                                  related_name='filter_questions')
    response = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='response_by')
    jobPost = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='job_info')

    def __str__(self):
        return f'{self.response}'


class OnlineTestModel(models.Model):
    culturalTest = models.URLField(verbose_name='Cultural Test', name='cultural_test')
    analyticalTest = models.URLField(verbose_name='Analytical Test', name='analytical_test')
    jobInfo = models.OneToOneField(JobPostModel, on_delete=models.CASCADE, related_name='job_info_online')

    def __str__(self):
        return f'{self.jobInfo}'


class PracticalTestModel(models.Model):
    practicalFile = models.FileField(verbose_name='Practical Test File', upload_to='users/files')
    testLink = models.URLField(verbose_name='Test link', blank=True)
    jobInfo = models.OneToOneField(JobPostModel, on_delete=models.CASCADE, related_name='practical_job_info')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_user_info')

    def __str__(self):
        return f'{self.jobInfo}'


"""
====Candidate section====
All candidate response will stored model section
online test response
practical test response
"""


class JobStatusModel(models.Model):
    status = models.CharField(max_length=50, blank=False, null=False)
    statusOrder = models.TextField()

    def __str__(self):
        return self.status


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

class UserJobAppliedModel(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_user')
    jobPostId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='applied_job_post_id')
    jobProgressStatus = models.ForeignKey(JobStatusModel, on_delete=models.CASCADE,
                                          related_name='job_applied_progress_status')
    # jobProgressStatus = models.CharField(max_length=30, choices=status, blank=True)
    appliedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.jobPostId}, {self.userId}'


class OnlineTestResponseModel(models.Model):
    analyticalTestMark = models.IntegerField(blank=True, verbose_name='Analytical Test Mark')
    analyticalTestScnSrt = models.ImageField(upload_to='online_test/analytical_test/', blank=True,
                                             verbose_name='Screenshot')
    practicalTestMark = models.IntegerField(blank=True, verbose_name='Practical Test Mark')
    practicalTestScnSrt = models.ImageField(upload_to='online_test/practical_test/', blank=True,
                                            verbose_name='Screenshot')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='online_response_user')
    appliedJob = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                      related_name='job_applied_online_response')
    submittedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.analyticalTestMark}, {self.practicalTestMark}'


class PracticalTestResponseModel(models.Model):
    practicalTestResFiles = models.FileField(upload_to='practical_test/response/', blank=True)
    practicalTestResLink = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_response_user')
    appliedJob = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
                                   related_name='job_applied_practical_response')
    submittedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.practicalTestResLink}   {self.practicalTestResFiles}'
