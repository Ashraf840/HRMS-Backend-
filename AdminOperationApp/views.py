import datetime
import calendar
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from UserApp.models import User, UserDepartmentModel, EmployeeInfoModel
from . import serializer
from . import models
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel, OnlineTestResponseModel, \
    PracticalTestModel
from rest_framework.permissions import IsAuthenticated
from UserApp.permissions import IsHrUser, IsAdminUser
from .utils import Util


class OnlineTestLinkView(generics.ListAPIView):
    """
    Online link will be visible for specific jobs
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.AdminOnlineTestLinkSerializer

    def get_queryset(self):
        id = self.kwargs['jobInfo']
        return OnlineTestModel.objects.filter(jobInfo_id=id)


class SendPracticalTestView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # admin permission required
    serializer_class = serializer.SendPracticalTestSerializer
    queryset = models.PracticalTestUserModel.objects.all()

    # def perform_create(self, serializer):
    #     p_id = self.kwargs['job_id']
    #     id = self.kwargs['id']
    #     serializer.save(user=User.objects.get(id=id),
    #                     practicalTestInfo=PracticalTestModel.objects.get(jobInfo__id=p_id))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            duration = int(request.data.get('duration'))
            user = User.objects.get(id=request.data.get('user'))
            # print(request.data.get('practicalTestInfo'))
            # print(models.PracticalTestUserModel.objects.get(id=request.data.get('practicalTestInfo')))
            # task = PracticalTestModel.objects.get(id=models.PracticalTestUserModel.objects.get(id=request.data.get('practicalTestInfo')))
            # print(task)
            email_body = f'Hi  {user.full_name} submit the task before {datetime.date.today() + datetime.timedelta(duration)}'
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Update'}
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminDashboardView(generics.ListAPIView):
    """
    Admin dashboard for recruitment site.
    recent posted jobs
    recent applicants,
    graph data,
    Barchart data
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.AdminDashboardSerializer
    queryset = UserJobAppliedModel.objects.all()[:5]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data

        # department graph data calculation
        departments = UserDepartmentModel.objects.filter()
        departmentGraph = []
        for dept in departments:
            deptApplicant = UserJobAppliedModel.objects.filter(
                jobPostId__department__department=dept.department).count()
            totalApplicant = UserJobAppliedModel.objects.all().count()
            percentage = int((deptApplicant * 100) / totalApplicant)
            graph = (
                (dept.department, percentage)
            )
            departmentGraph.append(graph)

        # Barchart data calculation
        months = []
        applicantByMonth = []

        month_number = datetime.date.today().month

        year = self.kwargs['year']
        for month in range(1, 13):
            # if month > 0:
            #     yearCheck = year
            #
            # else:
            #     yearCheck = year - 1
            applicant = UserJobAppliedModel.objects.filter(appliedDate__month=month,
                                                           appliedDate__year=year).count()

            applicantByMonth.append(applicant)
            months.append(calendar.month_name[month])
            # print(applicant)

        barCart = {
            'months': months,
            'applicantByMonth': applicantByMonth
        }

        # recent job section
        jobs = JobPostModel.objects.all()[:5]
        recentJobs = []
        for job in jobs:
            totalApplied = UserJobAppliedModel.objects.filter(jobPostId=job.id).count()
            jobDict = {
                'jobTitle': job.jobTitle,
                'totalApplied': totalApplied,
                'status': job.is_active
            }
            recentJobs.append(jobDict)

        diction = {
            'departmentGraph': departmentGraph,
            'barCart': barCart,
            'recentJobs': recentJobs

        }
        responseData.append(diction)
        # print(responseData)
        return Response(responseData)


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
    queryset = UserJobAppliedModel.objects.filter(jobProgressStatus__status='F2F Interview')

    # def get(self, request, *args, **kwargs):
    #     data = self.get_serializer(self.get_queryset(), many=True)
    #     print(data)
    #     return Response(data)


class MarkingDuringInterviewView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    serializer_class = serializer.MarkingDuringInterviewSerializer
    queryset = models.MarkingDuringInterviewModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(interviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        checkStatus = UserJobAppliedModel.objects.get(userId_id=request.data['user'])
        if checkStatus.jobProgressStatus.status == 'F2F Interview':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'This candidate is not selected for F2F Interview'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
