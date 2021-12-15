from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializer
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel
from rest_framework.permissions import IsAuthenticated
from UserApp.permissions import IsHrUser


# Create your views here.
class AppliedUserDetailsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsHrUser]
    serializer_class = serializer.AppliedUserDetailsSerializer

    def get_queryset(self):
        queryset = UserJobAppliedModel.objects.all()
        # print(queryset.count())
        return queryset

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


class AdminJobListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsHrUser]
    serializer_class = serializer.AdminJobListSerializer

    def get_queryset(self):
        return JobPostModel.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data

        totalJob = self.get_queryset().count()


        diction = {
            'totalJob': totalJob,

        }
        responseData.append(diction)
        return Response(responseData)
