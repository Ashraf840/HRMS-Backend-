from django.db import models
from UserApp.models import User
from RecruitmentManagementApp.models import PracticalTestModel, UserJobAppliedModel


# Create your models here.

class PracticalTestUserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practical_test_user')
    practicalTestInfo = models.ForeignKey(PracticalTestModel, on_delete=models.CASCADE,
                                          related_name='practical_test_info')
    duration = models.IntegerField(blank=True, default=2)

    def __str__(self):
        return f'{self.user}, {self.practicalTestInfo}'


markingValue = (
    ('5', 'A'),
    ('4', 'B'),
    ('3', 'C'),
    ('2', 'D'),
    ('1', 'E'),
    ('0', 'F'),
)


class MarkingDuringInterviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marking_during_interview_candidate_user')
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
        intMark = []
        for i in marks:
            if i >= '0':
                temp += 1
                intMark.append(int(i))

        # print(temp)
        res = sum(intMark)/temp
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
        return f'user: {self.user.full_name}, Feedback: {self.summary()}'
