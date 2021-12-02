from django.db import models
from UserApp.models import UserDepartmentModel, User


# Create your models here.

class JobPostModel(models.Model):
    shiftOption = (
        ('day', 'Day'),
        ('night', 'Night'),
    )
    jobType = (
        ('per_time', 'Per Time'),
        ('full_time', 'Full Time'),
        ('internship', 'Internship'),
    )
    jobTitle = models.CharField(verbose_name='Job Title', max_length=100)
    lastDateOfApply = models.DateField()
    startDate = models.DateField()
    endDate = models.DateField()
    level = models.CharField(max_length=255, null=True)
    shift = models.CharField(verbose_name='Shift', max_length=10, choices=shiftOption)
    location = models.CharField(verbose_name='location', max_length=255)
    department = models.ForeignKey(UserDepartmentModel, on_delete=models.CASCADE, related_name='department_jobPost',
                                   null=True)
    vacancies = models.IntegerField()
    jobType = models.CharField(verbose_name="job type",max_length=50,choices=jobType)
    jobDescription = models.TextField(null=True)
    # uploadCV = models.FileField(upload_to='user/')
    user = models.ForeignKey(User,verbose_name='user',on_delete=models.CASCADE,related_name='job_post_model')

    def __str__(self):
        return f'{self.jobTitle} {self.shift}'


class UserJobAppliedModel(models.Model):
    jobPostId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='job_post_id')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_user')

    def __str__(self):
        return f'{self.jobPostId}, {self.userId}'
