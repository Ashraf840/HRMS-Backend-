import datetime, calendar
from django.db.models import Q
from rest_framework import generics, permissions, status, pagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from UserApp.models import User, UserDepartmentModel, EmployeeInfoModel
from . import serializer
from . import models
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel, OnlineTestResponseModel, \
    FilterQuestionsResponseModelHR, PracticalTestResponseModel, DocumentSubmissionModel, ReferenceInformationModel
from rest_framework.permissions import IsAuthenticated
from UserApp.permissions import IsHrUser
from .utils import Util


class Pagination(pagination.PageNumberPagination):
    """
    Pagination classes
    """
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 5


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
    """
    set and send practical test link to the candidate
    """
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


class PracticalTestMarkUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    practical test mark will be given and evaluate candidate practical test mark
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.PracticalTestMarkInputSerializer
    # queryset = models.PracticalTestMarkInputModel.objects.filter(jobApplication_id='jobApplication')
    lookup_field = 'jobApplication'

    def get_queryset(self):
        application_id = self.kwargs['jobApplication']
        queryset = models.PracticalTestMarkInputModel.objects.filter(jobApplication_id=application_id)
        return queryset

    def perform_update(self, serializer):
        instance = self.get_object()  # instance before update
        print(instance)
        self.request.data.get("jobApplication", None)  # read data from request
        if self.request.user.is_authenticated:
            updated_instance = serializer.save(markAssignBy=self.request.user)
        else:
            updated_instance = serializer.save()
        return updated_instance

    # def perform_update(self, serializer):
    #     application_id = self.kwargs['jobApplication']
    #     serializer.save(jobApplication=UserJobAppliedModel.objects.get(id=application_id),
    #                     markAssignBy=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)


class RecruitmentAdminApplicantListView(generics.ListAPIView):
    """
    Recruitment job list for recruitment admin dashboard
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.AdminDashboardSerializer
    queryset = UserJobAppliedModel.objects.all().order_by('-id')
    pagination_class = Pagination


class RecruitmentAdminGraphView(generics.ListAPIView):
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
        # serializer = self.get_serializer(self.get_queryset(), many=True)
        # response = serializer.data
        responseData = []
        # department graph data calculation
        departments = UserDepartmentModel.objects.filter()
        department_list = []
        department_percent = []
        for dept in departments:
            deptApplicant = UserJobAppliedModel.objects.filter(
                jobPostId__department__department=dept.department).count()
            totalApplicant = UserJobAppliedModel.objects.all().count()
            percentage = int((deptApplicant * 100) / totalApplicant)
            department_list.append(dept.department)
            department_percent.append(percentage)
            # graph = (
            #     (dept.department, percentage)
            # )
        departmentGraph = {
            'department_list': department_list,
            'department_percent': department_percent
        }

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
        jobs = JobPostModel.objects.all().order_by('-lastDateOfApply')[:5]
        recentJobs = []
        for job in jobs:
            totalApplied = UserJobAppliedModel.objects.filter(jobPostId=job.id).count()
            jobDict = {
                'jobId': job.id,
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

    def get_queryset(self):
        queryset = UserJobAppliedModel.objects.all()
        search = self.request.query_params.get('search')
        department = self.request.query_params.get('department')
        shift = self.request.query_params.get('shift')
        job_type = self.request.query_params.get('job_type')
        return queryset.filter((Q(userId__full_name__icontains=search) |
                                Q(jobPostId__jobTitle__icontains=search) |
                                Q(jobPostId__department__department__icontains=search) |
                                Q(jobPostId__jobType__icontains=search) |
                                Q(jobPostId__shift__icontains=search)),
                               Q(jobPostId__shift__icontains=shift),
                               Q(jobPostId__department__department__icontains=department),
                               Q(jobPostId__jobType__icontains=job_type)
                               )

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
        queryset = JobPostModel.objects.all()
        search = self.request.query_params.get('search')
        jobType = self.request.query_params.get('jobType')
        department = self.request.query_params.get('department')
        # expire = self.request.query_params.get('expire')
        shift = self.request.query_params.get('shift')

        return queryset.filter(
            (Q(jobType__icontains=search) | Q(shift__icontains=search) | Q(department__department__icontains=search) |
             Q(jobTitle__icontains=search)),
            Q(jobType__icontains=jobType), Q(shift__icontains=shift),
            Q(department__department__icontains=department))

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


class RecruitmentNewApplicantView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.RecruitmentNewApplicantSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        job_id = self.kwargs['job_id']
        queryset = UserJobAppliedModel.objects.filter(jobPostId_id=job_id).order_by('-appliedDate')
        return queryset.filter(Q(jobPostId__jobType__icontains=search) | Q(jobPostId__shift__icontains=search) |
                               Q(jobPostId__jobTitle__icontains=search) | Q(userId__full_name__icontains=search))

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data
        return Response(responseData)


class FilterQuestionResponseListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.FilterQuestionResponseListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        job_id = self.kwargs['job_id']
        queryset = FilterQuestionsResponseModelHR.objects.filter(user=user_id, jobPost=job_id)
        return queryset


class AdminAppliedCandidateOnlineResView(generics.ListAPIView):
    """
    Online test response list
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AdminAppliedCandidateOnlineResSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        queryset = OnlineTestResponseModel.objects.filter(appliedJob__jobPostId_id=job_id)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #


class TestAdminAppliedCandidateOnlineResView(generics.ListAPIView):
    serializer_class = serializer.TestAdminAppliedCandidateOnlineResSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        search = self.request.query_params.get('search')
        queryset = UserJobAppliedModel.objects.filter(jobPostId_id=job_id)
        return queryset.filter(Q(userId__full_name__icontains=search)| Q(userId__email__icontains=search))


class RecruitmentPracticalTestResponseView(generics.ListAPIView):
    """
    Recruitment practical test response and marks
    """
    serializer_class = serializer.RecruitmentPracticalTestResponseSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        queryset = PracticalTestResponseModel.objects.filter(appliedJob__jobPostId_id=job_id)
        return queryset


class AdminInterviewerListView(generics.ListAPIView):
    """
    selected for interview stage
    """
    serializer_class = serializer.AdminInterviewerListSerializer
    queryset = UserJobAppliedModel.objects.filter(jobProgressStatus__status='F2F Interview')

    # def get(self, request, *args, **kwargs):
    #     data = self.get_serializer(self.get_queryset(), many=True)
    #     print(data)
    #     return Response(data)


class MarkingDuringInterviewView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.MarkingDuringInterviewSerializer
    queryset = models.MarkingDuringInterviewModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(interviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        checkStatus = UserJobAppliedModel.objects.get(userId_id=request.data['candidate'],
                                                      id=request.data['appliedJob'])
        if checkStatus.jobProgressStatus.status == 'F2F Interview':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'This candidate is not selected for F2F Interview'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)


# class ChangeEmailDuringOnboardingView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Provide a official Email to the selected candidate
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.UpdateEmailDuringOnboardingSerializer
#     queryset = User.objects.all()
#     lookup_field = 'id'
#
#     def update(self, request, *args, **kwargs):
#         id = self.kwargs['id']
#         personalEmail = User.objects.get(id=id).email
#         # print(personalEmail)
#         # officialEmail = request.data['email']
#         try:
#             employeeInfo = EmployeeInfoModel.objects.get(user__id=id)
#         except:
#             employeeInfo = EmployeeInfoModel.objects.create(user_id=id, personalEmail=personalEmail)
#         print(employeeInfo.personalEmail)
#         employeeInfo.personalEmail = personalEmail
#         employeeInfo.save()
#         print(employeeInfo.personalEmail)
#
#         return Response(request.data, status=status.HTTP_201_CREATED)
#
#
#         # print(officialEmail)

class AddEmployeeInfoDuringOnboardView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AddEmployeeInfoDuringOnboardSerializer
    queryset = EmployeeInfoModel.objects.all()

    def perform_create(self, serializer):
        queryset = EmployeeInfoModel.objects.filter(user=User.objects.get(id=self.kwargs['id']))
        if queryset.exists():
            raise ValidationError({'detail': 'Employee information already Created'})
        serializer.save(user=User.objects.get(id=self.kwargs['id']))

    def create(self, request, *args, **kwargs):
        id = self.kwargs['id']
        serializer = self.get_serializer(data=request.data)
        personalInfo = User.objects.get(id=id)
        setEmail = personalInfo.email
        personalInfo.email = request.data['email']
        personalInfo.save()
        request.data._mutable = True
        request.data['email'] = setEmail
        request.data._mutable = False
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InterviewTimeScheduleView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.InterviewTimeScheduleSerializer
    queryset = models.InterviewTimeScheduleModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(scheduleBy=self.request.user)


"""
=======================Document section =======================
"""


class AdminDocumentVerificationView(generics.ListAPIView):
    serializer_class = serializer.AdminDocumentVerificationSerializer

    def get_queryset(self):
        return DocumentSubmissionModel.objects.filter(applied_job=self.kwargs['applied_job'])

    def list(self, request, *args, **kwargs):
        applicationId = self.kwargs['applied_job']
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data
        references = ReferenceInformationModel.objects.filter(applied_job=applicationId)
        jobApplication = UserJobAppliedModel.objects.get(id=applicationId)
        jobDetails = JobPostModel.objects.get(id=jobApplication.jobPostId.id)
        jobName = jobDetails.jobTitle
        progressStatus = jobApplication.jobProgressStatus.status
        responseData.append({'references': references})
        responseData.append(
            {
                'jobTitle': jobName,
                'department': jobDetails.department.department,
                'progressStatus': progressStatus,

            }
        )

        return Response(responseData)

    # def retrieve(self, request, *args, **kwargs):
    #     applicationId = self.kwargs['applied_job']
    #
    #     serializer = self.get_serializer(self.get_object())
    #     print(serializer.data)
    #     return Response()


class GenerateAppointmentLetterView(generics.CreateAPIView):
    serializer_class = serializer.GenerateAppointmentLetterSerializer
    queryset = models.GenerateAppointmentLetterModel.objects.all()

    # def perform_create(self, serializer):
    #     serializer
    #     serializer.save(applicationId=)

    def create(self, request, *args, **kwargs):
        alreadyApplied = models.GenerateAppointmentLetterModel.objects.filter(
            applicationId=request.data['applicationId'])
        if alreadyApplied.count() < 1:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already created Appointment letter for this candidate'},
                        status=status.HTTP_208_ALREADY_REPORTED)


class AppointmentLetterInformationView(generics.ListAPIView):
    serializer_class = serializer.GenerateAppointmentLetterSerializer

    def get_queryset(self):
        applicationId = self.kwargs['applied_job']
        queryset = models.GenerateAppointmentLetterModel.objects.filter(applicationId=applicationId)
        return queryset

    def list(self, request, *args, **kwargs):
        applicationId = self.kwargs['applied_job']
        userInformation = UserJobAppliedModel.objects.get(id=applicationId)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data
        data = self.get_queryset().get()
        grossSalary = int(data.grossSalary)
        basicSalary = grossSalary * .5
        homeAllowance = basicSalary * .6
        medicalAllowance = basicSalary * .2
        transportAllowance = basicSalary * .2
        responseData.append({
            'grossSalary': grossSalary,
            'basicSalary': int(basicSalary),
            'homeAllowance': int(homeAllowance),
            'medicalAllowance': int(medicalAllowance),
            'transportAllowance': int(transportAllowance)
        })

        responseData.append({
            'applicantName': userInformation.userId.full_name,
            'location': userInformation.userId.location,
            'nid': userInformation.userId.nid,
            'jobTitle': userInformation.jobPostId.jobTitle,

        })

        return Response(responseData)
