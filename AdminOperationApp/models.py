from django.db import models
from django.db.models.signals import post_save, pre_delete,post_delete
from django.dispatch import receiver

from UserApp.models import User, UserDesignationModel
from RecruitmentManagementApp.models import PracticalTestModel, UserJobAppliedModel, PracticalTestResponseModel

# Create your models here.
markingValue = (
    ('5', 'A'),
    ('4', 'B'),
    ('3', 'C'),
    ('2', 'D'),
    ('1', 'E'),
    ('0', 'F'),
)


class PracticalTestUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_test_user')
    practicalTestInfo = models.ForeignKey(PracticalTestModel, on_delete=models.CASCADE,
                                          related_name='practical_test_info')
    duration = models.IntegerField(blank=True, default=2)

    def __str__(self):
        return f'{self.user}, {self.practicalTestInfo}'


class PracticalTestMarkInputModel(models.Model):
    jobApplication = models.OneToOneField(UserJobAppliedModel, on_delete=models.CASCADE,
                                          related_name='practical_test_application')
    markAssignBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mark_assigned_by_user',
                                     blank=True, null=True)
    testMark = models.CharField(choices=markingValue, max_length=2, blank=True, null=True)

    def __str__(self):
        return f'{self.id} {self.testMark}, {self.jobApplication}'


# Django signal
@receiver(post_save, sender=PracticalTestResponseModel)
def create_practical_test_mark(sender, instance, created, **kwargs):
    """
    Create practical test response mark instance while submitting practical test response
    """
    if created:
        data = UserJobAppliedModel.objects.get(job_applied_practical_response__id=instance.id)
        # print(data)
        PracticalTestMarkInputModel.objects.create(jobApplication=data)


@receiver(pre_delete, sender=PracticalTestResponseModel)
def delete_practical_test_mark(sender, instance, **kwargs):
    data = UserJobAppliedModel.objects.get(job_applied_practical_response__id=instance.id)
    PracticalTestMarkInputModel.objects.get(jobApplication_id=data.id).delete()


class MarkingDuringInterviewModel(models.Model):
    """
    Mark input during interview
    """
    candidate = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='marking_during_interview_candidate_user')
    appliedJob = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
                                   related_name='applied_job_user_applied_model')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='marking_during_interview_interviewer_user')
    behavior = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    personality = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    dressSense = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    professionalism = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    engSpeaking = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    eagerness = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    flexibility = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    technicalKnowledge = models.CharField(max_length=10, choices=markingValue, blank=True, null=True)
    expSalary = models.CharField(max_length=255, blank=True, null=True)
    expectedJoiningData = models.DateField(blank=True)
    comment = models.TextField(blank=True)

    def summary(self):
        marks = [self.behavior, self.personality, self.dressSense, self.professionalism, self.engSpeaking,
                 self.eagerness, self.flexibility, self.technicalKnowledge]
        temp = 0
        marks = list(filter(None, marks))
        intMark = []
        for i in marks:
            if int(i) >= 0:
                temp += 1
                intMark.append(int(i))

        # print(temp)
        res = sum(intMark) / temp
        response = ''
        if 4.5 <= res <= 5:
            response = 'Good Fit'
        elif res > 4:
            response = 'Suitable'
        elif res > 3:
            response = 'Average'
        elif res < 3:
            response = 'Not Fit'

        return response

    def __str__(self):
        return f'user: {self.candidate.full_name}, Feedback: {self.summary()}'


class InterviewTimeScheduleModel(models.Model):
    """
    Time scheduling for interview
    """
    applicationId = models.ForeignKey(UserJobAppliedModel, on_delete=models.SET_NULL,
                                      related_name='application_id_applied_job', null=True)
    interviewer = models.ForeignKey(UserDesignationModel, on_delete=models.SET_NULL,
                                    related_name='interviewer_designation', null=True)
    candidate = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='candidate_interview_user', null=True,
                                  blank=True)
    scheduleBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='meeting_scheduled_user',
                                   null=True)
    interviewDate = models.DateField()
    interviewTime = models.TimeField()
    interviewLocation = models.TextField()
    scheduleAssignDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.interviewDate} - {self.interviewer}'


class FinalSalaryNegotiationModel(models.Model):
    assignedBy = models.ForeignKey(User, on_delete=models.CASCADE)


class GenerateAppointmentLetterModel(models.Model):
    applicationId = models.ForeignKey(UserJobAppliedModel, on_delete=models.CASCADE,
                                      related_name='application_id_job_applied_user')
    subjectLine = models.CharField(max_length=255, blank=True)
    joiningDate = models.DateField()
    grossSalary = models.IntegerField()
    jobDescription = models.TextField()
    termsCondition = models.TextField()

    def __str__(self):
        return f'{self.applicationId.userId.full_name} - {self.applicationId.jobPostId.jobTitle}'


