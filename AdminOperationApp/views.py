import datetime

from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from UserApp.models import User
from . import serializer
from . import models
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel, OnlineTestResponseModel, \
    PracticalTestModel
from rest_framework.permissions import IsAuthenticated
from UserApp.permissions import IsHrUser

from .utils import Util


class OnlineTestLinkView(generics.RetrieveAPIView):
    """
    Online link will be visible for specific jobs
    """
    serializer_class = serializer.AdminOnlineTestLinkSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return OnlineTestModel.objects.filter(jobInfo_id=id)


class SendPracticalTestView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.SendPracticalTestSerializer
    queryset = models.PracticalTestUserModel.objects.all()

    def perform_create(self, serializer):
        p_id = self.kwargs['p_id']
        id = self.kwargs['id']
        serializer.save(user=User.objects.get(id=id), practicalTestInfo=PracticalTestModel.objects.get(id=p_id))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            duration = int(request.data.get('duration'))
            user = User.objects.get(id=self.kwargs['id'])
            email_body = f'Hi  {user.full_name} submit the task before {datetime.date.today() + datetime.timedelta(duration)} '
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Update'}
            Util.send_email(data)

        return super().create(request)


class AppliedUserDetailsView(generics.ListAPIView):
    """
    admin will see the all applied user details and sort summary of recruitment like total applicant, hired,
    rejected or on shortlisted applicant.
    """
    permission_classes = [IsAuthenticated, IsHrUser]
    serializer_class = serializer.AppliedUserDetailsSerializer
    queryset = UserJobAppliedModel.objects.all()

    # def get_queryset(self):
    #     queryset = UserJobAppliedModel.objects.all()
    #     # print(queryset.count())
    #     return queryset
    # customizing default list view to provide more specific information like total applicant,shortlisted
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data
        totalApplicant = self.get_queryset().count()
        rejectedCandidate = self.get_queryset().filter(jobProgressStatus__status='rejected').count()
        shortListedCandidate = self.get_queryset().filter(
            Q(jobProgressStatus__status='online') | Q(jobProgressStatus__status='practical') | Q(
                jobProgressStatus__status='document')
        ).count()
        hiredCandidate = self.get_queryset().filter(jobProgressStatus__status='hired').count()
        diction = {
            'totalApplicant': totalApplicant,
            'shortListedCandidate': shortListedCandidate,
            'rejectedCandidate': rejectedCandidate,
            'hiredCandidate': hiredCandidate

        }
        responseData.append(diction)
        return Response(responseData)


class AdminJobListView(generics.ListAPIView):
    """
    All job List will be shown here for admin
    """
    permission_classes = [IsAuthenticated, IsHrUser]
    serializer_class = serializer.AdminJobListSerializer

    def get_queryset(self):
        return JobPostModel.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data

        totalJob = self.get_queryset().count()
        totalInterview = UserJobAppliedModel.objects.filter(jobProgressStatus__status='interview').count()
        totalHired = UserJobAppliedModel.objects.filter(jobProgressStatus__status='hired').count()
        totalApplicant = UserJobAppliedModel.objects.all().count()

        diction = {
            'totalJob': totalJob,
            'totalInterview': totalInterview,
            'totalHired': totalHired,
            'totalApplicant': totalApplicant,
        }
        responseData.append(diction)
        return Response(responseData)


class AdminAppliedCandidateOnlineResView(generics.ListAPIView):
    serializer_class = serializer.AdminAppliedCandidateOnlineResSerializer
    queryset = OnlineTestResponseModel.objects.all()


class AdminInterviewerListView(generics.ListAPIView):
    serializer_class = serializer.AdminInterviewerListSerializer
    queryset = UserJobAppliedModel.objects.all()
