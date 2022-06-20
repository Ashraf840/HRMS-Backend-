import calendar
import datetime
import os

import HRM_Admin.models
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.template.loader import render_to_string
from django.templatetags.static import static
from RecruitmentManagementApp.models import (CandidateJoiningFeedbackModel,
                                             DocumentSubmissionModel,
                                             FilterQuestionsResponseModelHR,
                                             JobPostModel, JobStatusModel,
                                             OfficialDocumentsModel,
                                             OnlineTestModel,
                                             OnlineTestResponseModel,
                                             PracticalTestResponseModel,
                                             ReferenceInformationModel,
                                             UserJobAppliedModel)
from rest_framework import generics, pagination, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from TFHRM.settings import BASE_DIR
from UserApp import permissions as customPermission
from UserApp.models import User, UserDepartmentModel

from AdminOperationApp import utils

from . import models, serializer
from .utils import Util


from AdminOperationApp import utils

class Pagination(pagination.PageNumberPagination):
    """
    Pagination classes
    """
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 5


class OfficialDocStoreView(generics.ListCreateAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.OfficialDocStoreSerializer
    queryset = models.OfficialDocStore.objects.all()

    def list(self, request, *args, **kwargs):
        ser = self.get_serializer(self.get_queryset(), many=True)
        responseData = ser.data
        # if self.request.user.is_candidate:
        #
        # else:
        #     return Response(responseData)
        try:
            id = self.kwargs['application_id']
            try:
                appointmentLetter = OfficialDocumentsModel.objects.get(applicationId=id)
                print(appointmentLetter)
                responseData.append(
                    {'allow_candidate_access': appointmentLetter.allow_applicant_access})
            except:
                responseData.append({'docName': 'Appointment Letter', 'docFile': ''})

            return Response(responseData)
        except:
            return Response(responseData)


class OnlineTestLinkView(generics.ListCreateAPIView):
    """
    Online link will be visible for specific jobs
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.AdminOnlineTestLinkSerializer

    def get_queryset(self):
        id = self.kwargs['jobInfo']
        return OnlineTestModel.objects.filter(jobInfo_id=id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OnlineTestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update online test
    """
    permission_classes = [customPermission.EmployeeAdminAuthenticated]
    serializer_class = serializer.AdminOnlineTestLinkSerializer
    queryset = OnlineTestModel.objects.all()
    lookup_field = 'id'


class RejectCandidateStatusView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [customPermission.EmployeeAdminAuthenticated]
    serializer_class = serializer.JobStatusRejectSerializer
    queryset = UserJobAppliedModel.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        applicationData = UserJobAppliedModel.objects.get(id=self.kwargs['id'])
        status = JobStatusModel.objects.all()
        applicationData.jobProgressStatus = status.get(status='Rejected')
        applicationData.save()
        """
        Email functionality
        """
        email_subject=f'Status of the Screening Test | ' + applicationData.jobPostId.jobTitle.capitalize() + ' | TechForing'
        applicantName=applicationData.userId.full_name
        email_body=render_to_string('emailTemplate/rejected_message.html', 
                                {'applicantName':applicantName, 'jobPosition': applicationData.jobPostId.jobTitle.capitalize()})
        data = {'email_body': email_body, 'to_email': self.request.user.email,
                    'email_subject': email_subject}
        utils.Util.send_email_body(data)

        return Response({'detail': 'rejected'})


class SendPracticalTestView(generics.ListCreateAPIView):
    """
    set and send practical test link to the candidate
    """
    permission_classes = [customPermission.Authenticated]  # admin permission required
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
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.PracticalTestMarkInputSerializer
    lookup_field = 'jobApplication'

    def get_queryset(self):
        application_id = self.kwargs['jobApplication']
        queryset = models.PracticalTestMarkInputModel.objects.filter(jobApplication_id=application_id)
        return queryset

    def perform_update(self, serializer):
        instance = self.get_object()  # instance before update
        # print(instance)
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
    queryset = UserJobAppliedModel.objects.all().order_by('-id')[:5]

    def list(self, request, *args, **kwargs):
        responseData = []
        departments = UserDepartmentModel.objects.filter()
        department_list = []
        department_percent = []
        for dept in departments:
            deptApplicant = UserJobAppliedModel.objects.filter(
                jobPostId__department__department=dept.department).count()
            totalApplicant = UserJobAppliedModel.objects.all().count()
            if totalApplicant == 0:
                percentage = 0
            else:
                percentage = int((deptApplicant * 100) / totalApplicant)
            department_percent.append(percentage)
            department_list.append(dept.department)
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
            applicant = UserJobAppliedModel.objects.filter(appliedDate__month=month,
                                                           appliedDate__year=year).count()

            applicantByMonth.append(applicant)
            months.append(calendar.month_name[month])

        barCart = {
            'months': months,
            'applicantByMonth': applicantByMonth
        }

        # recent job section
        jobs = JobPostModel.objects.all().order_by('-id')[:5]
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
        return Response(responseData)


class RecruitmentAdminApplicantListView(generics.ListAPIView):
    """
    Recruitment job list for recruitment admin dashboard
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.AdminDashboardSerializer
    queryset = UserJobAppliedModel.objects.all().order_by('-id')
    pagination_class = Pagination


class AdminJobListView(generics.ListAPIView):
    """
    All job List will be shown here for admin
    """
    permission_classes = [IsAuthenticated, customPermission.IsHrUser]
    serializer_class = serializer.AdminJobListSerializer

    def get_queryset(self):
        queryset = JobPostModel.objects.all().order_by('-postDate')
        try:
            search = self.request.query_params.get('search')
            jobType = self.request.query_params.get('jobType')
            department = self.request.query_params.get('department')
            # expire = self.request.query_params.get('expire')
            shift = self.request.query_params.get('shift')

            return queryset.filter(
                (Q(jobType__icontains=search) | Q(shift__icontains=search) | Q(
                    department__department__icontains=search) |
                 Q(jobTitle__icontains=search)),
                Q(jobType__icontains=jobType), Q(shift__icontains=shift),
                Q(department__department__icontains=department))
        except:
            return queryset

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


class AppliedUserDetailsView(generics.ListAPIView):
    """
    admin will see the all applied user details and sort summary of recruitment like total applicant, hired,
    rejected or on shortlisted applicant.
    """
    permission_classes = [IsAuthenticated, customPermission.IsHrUser]
    serializer_class = serializer.AppliedUserDetailsSerializer
    queryset = UserJobAppliedModel.objects.all()

    def get_queryset(self):
        queryset = UserJobAppliedModel.objects.all().order_by('-appliedDate')
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


class RecruitmentNewApplicantView(generics.ListAPIView):
    permission_classes = [customPermission.Authenticated]
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
    permission_classes = [customPermission.Authenticated]
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
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.AdminAppliedCandidateOnlineResSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        queryset = OnlineTestResponseModel.objects.filter(appliedJob__jobPostId_id=job_id)
        return queryset


class TestAdminAppliedCandidateOnlineResView(generics.ListAPIView):
    serializer_class = serializer.TestAdminAppliedCandidateOnlineResSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        search = self.request.query_params.get('search')
        queryset = UserJobAppliedModel.objects.filter(jobPostId_id=job_id)
        return queryset.filter(Q(userId__full_name__icontains=search) | Q(userId__email__icontains=search))


class RecruitmentPracticalTestResponseView(generics.ListAPIView):
    """
    Recruitment practical test response and marks
    """
    serializer_class = serializer.RecruitmentPracticalTestResponseSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        search = self.request.query_params.get('search')
        queryset = PracticalTestResponseModel.objects.filter(appliedJob__jobPostId_id=job_id,
                                                             appliedJob__jobProgressStatus__status='Practical Test')
        return queryset.filter(Q(user__email__icontains=search) | Q(user__full_name__icontains=search))


class AdminInterviewerListView(generics.ListAPIView):
    """
    selected for interview stage
    """
    permission_classes = [customPermission.EmployeeAdminAuthenticated]
    serializer_class = serializer.AdminInterviewerListSerializer

    def get_queryset(self):
        jobId = self.kwargs['job_id']
        queryset = UserJobAppliedModel.objects.filter(jobProgressStatus__status='F2F Interview', jobPostId_id=jobId)
        try:
            search = self.request.query_params.get('search')
            return queryset.filter(Q(userId__full_name__icontains=search) |
                                   Q(userId__email__icontains=search))
        except:
            return queryset

#update admin interviewer list
class PolicySentView(generics.ListCreateAPIView):
    permission_classes = [customPermission.EmployeeAdminAuthenticated]
    serializer_class = serializer.PolicySerializer
    lookup_field= 'applicationId' #applicant id
  
    def get_queryset(self):
        applicationId=self.kwargs['applicationId']
        queryset = models.PolicySentModel.objects.filter(applicationId=applicationId)
        return queryset
    def perform_create(self, serializer):
        applied=UserJobAppliedModel.objects.get(id=self.kwargs['applicationId'])
        serializer.save(applicationId=applied)
    def create(self, request, *args, **kwargs):
        #restriction for only one policy sent and send email to applicant
        if models.PolicySentModel.objects.filter(applicationId=self.kwargs['applicationId']).exists():
            return Response({'message':'Policy already sent'},status=status.HTTP_400_BAD_REQUEST)
        else:
            #send mail to applicant
            #get applicant data
            applicant=UserJobAppliedModel.objects.get(id=self.kwargs['applicationId'])
            applicant_email=applicant.userId.email
            applicant_name=applicant.userId.full_name
            applicant_job=applicant.jobPostId.jobTitle
            # email_body = f'Hi {applicant_name},\n' \
            #          f'Congratulation we have moved you to the next phase. We have sent you an attachment pdf of our policy please\n' \
            #          f'have a careful look at the attachment.\n' \
            #          f'Regads,\n' \
            #          f'HR,\n' \
            #          f'Techforing,\n' \
            email_body=render_to_string('emailTemplate/hrpolicy.html',{'applicant_name':applicant_name})
            email_subject=f' NDA & NCA from TechForing Career | {applicant_job}'
            data = {'email_body': email_body, 'to_email': applicant_email,
                'email_subject': email_subject, 'file_path': BASE_DIR/'static/Terms_And_Conditions.pdf'}
            #attach file to email 
            Util.send_email_attach_body(data)
            return super(PolicySentView, self).create(request, *args, **kwargs)

    
    

class MarkingDuringInterviewView(generics.ListCreateAPIView):
    permission_classes = [customPermission.Authenticated]
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
            # Email integrations
            # HR policy and other documents agree
            # doc_permission = serializer.data['docsPermission']
            # if doc_permission:
            # email_body = 'Please chek your portal, if you are agree the plese send us ur feedback ASAP' \
            #              'Thanks & Regards,\n' \
            #              'HR Department\n' \
            #              'TechForing Limited.\n' \
            #              'www.techforing.com' \
            #              f'Office Address: House: 149 (4th floor), Lane: 1, Baridhara DOHS, Dhaka.\n'
            # data = {'email_body': email_body, 'to_email': checkStatus.userId.email,
            #         'email_subject': 'Techforing|Document check'}
            # Util.send_email(data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'This candidate is not selected for F2F Interview'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)


# class ChangeEmailDuringOnboardingView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Provide a official Email to the selected candidate
#     """
#     permission_classes = [customPermission.Authenticated]
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

# class AddEmployeeInfoDuringOnboardView(generics.CreateAPIView):
#     permission_classes = [customPermission.Authenticated]
#     serializer_class = serializer.AddEmployeeInfoDuringOnboardSerializer
#     queryset = EmployeeInfoModel.objects.all()
#
#     def perform_create(self, serializer):
#         queryset = EmployeeInfoModel.objects.filter(user=User.objects.get(id=self.kwargs['id']))
#         if queryset.exists():
#             raise ValidationError({'detail': 'Employee information already Created'})
#         serializer.save(user=User.objects.get(id=self.kwargs['id']))
#
#     def create(self, request, *args, **kwargs):
#         id = self.kwargs['id']
#         serializer = self.get_serializer(data=request.data)
#         personalInfo = User.objects.get(id=id)
#         setEmail = personalInfo.email
#         personalInfo.email = request.data['email']
#         personalInfo.save()
#         request.data._mutable = True
#         request.data['email'] = setEmail
#         request.data._mutable = False
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class InterviewTimeScheduleView(generics.ListCreateAPIView):
    """
    Interview Schedule for a candidate
    """
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.InterviewTimeScheduleSerializer
    queryset = models.InterviewTimeScheduleModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(scheduleBy=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        applicationData = UserJobAppliedModel.objects.get(id=serializer.data.get('applicationId'))
        # print(applicationData)
        jobStatus = JobStatusModel.objects.all()

        # time conversion
        def time_convert(str1):
            time = datetime.datetime.strptime(str1, "%H:%M:%S")
            return time.strftime("%I:%M %p")

        # email sending function
        def send_email_office(interview_type, format):
            if interview_type == 'virtual':
                if format == 'new':
                    email_subject=f'Invitation For F2F Interview | ' + applicationData.jobPostId.jobTitle.capitalize() + ' | TechForing'
                    applicant_name=applicationData.userId.full_name
                    email_body=render_to_string('emailTemplate/interview/virtual_new_interview.html', 
                                {'applicant_name':applicant_name, 'jobPosition': applicationData.jobPostId.jobTitle.capitalize(), 'interview_location': interview_type.capitalize(), 'interview_date': serializer.data["interviewDate"], 'interview_time': time_convert(serializer.data["interviewTime"]), 'meeting_link': serializer.data["interviewLocation"]})
                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                                'email_subject': email_subject}
                    utils.Util.send_email_body(data)

                else:
                    email_subject=f'Interview Schedule | ' + applicationData.jobPostId.jobTitle.capitalize() + ' | TechForing'
                    applicant_name=applicationData.userId.full_name
                    email_body=render_to_string('emailTemplate/interview/virtual_update_interview.html', 
                                {'applicant_name':applicant_name, 'jobPosition': applicationData.jobPostId.jobTitle.capitalize(), 'interview_location': interview_type.capitalize(), 'interview_date': serializer.data["interviewDate"], 'interview_time': time_convert(serializer.data["interviewTime"]), 'meeting_link': serializer.data["interviewLocation"]})
                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                                'email_subject': email_subject}
                    utils.Util.send_email_body(data)
            else:
                if format == 'new':
                    email_subject=f'Invitation For F2F Interview | ' + applicationData.jobPostId.jobTitle.capitalize() + ' | TechForing'
                    applicant_name=applicationData.userId.full_name
                    email_body=render_to_string('emailTemplate/interview/office_new_interview.html', 
                                {'applicant_name':applicant_name, 'jobPosition': applicationData.jobPostId.jobTitle.capitalize(), 'interview_location': interview_type.capitalize(), 'interview_date': serializer.data["interviewDate"], 'interview_time': time_convert(serializer.data["interviewTime"])})
                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                                'email_subject': email_subject}
                    utils.Util.send_email_body(data)

                else:
                    email_subject=f'Interview Schedule | ' + applicationData.jobPostId.jobTitle.capitalize() + ' | TechForing'
                    applicant_name=applicationData.userId.full_name
                    email_body=render_to_string('emailTemplate/interview/office_update_interview.html', 
                                {'applicant_name':applicant_name, 'jobPosition': applicationData.jobPostId.jobTitle.capitalize(), 'interview_location': interview_type.capitalize(), 'interview_date': serializer.data["interviewDate"], 'interview_time': time_convert(serializer.data["interviewTime"])})
                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                                'email_subject': email_subject}
                    utils.Util.send_email_body(data)

        applicantStatus = applicationData.jobProgressStatus.status
        if applicantStatus == 'Practical Test' or applicantStatus == 'Online Test' or applicantStatus == 'F2F Interview':
            if not applicantStatus == 'F2F Interview':
                applicationData.jobProgressStatus = jobStatus.get(status='F2F Interview')
                applicationData.save()

            interviewSchedule = applicationData.application_id_applied_job.all().count()
            # mail sending using function
            location = serializer.data.get('interviewLocationType')
            if interviewSchedule > 1:
                send_email_office(location, 'old')
            else:
                send_email_office(location, 'new')


        else:
            if applicationData.jobProgressStatus.status == 'new':
                applicationData.jobProgressStatus = jobStatus.get(status='F2F Interview')
                applicationData.save()
                location = serializer.data.get('interviewLocationType')
                interviewSchedule = applicationData.application_id_applied_job.all().count()
                if interviewSchedule > 1:
                    send_email_office(location, 'old')
                else:
                    send_email_office(location, 'new')

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InterviewTimeUpdateView(generics.ListAPIView):
    """
    Interview schedule update
    """
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.InterviewTimeScheduleSerializer
    lookup_field = 'applicationId_id'

    def get_queryset(self):
        queryset = models.InterviewTimeScheduleModel.objects.filter(
            applicationId_id=self.kwargs['applicationId_id']).order_by('-id')[:1]
        return queryset

    def perform_update(self, serializer):
        serializer.save(scheduleBy=self.request.user)

        applicationData = models.InterviewTimeScheduleModel.objects.filter(
            applicationId_id=self.kwargs['applicationId_id']).order_by('-id')[:1]

        email_body = 'Hi ' + applicationData.applicationId.userId.full_name + \
                     f'New schedule updated check portal' \
                     'Prepare yourself.'

        data = {'email_body': email_body, 'to_email': applicationData.applicationId.userId.email,
                'email_subject': 'Status of the Screening Test'}
        Util.send_email(data)


"""
=======================salary section =======================
"""


class FinalSalaryView(generics.CreateAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.FinalSalarySerializer
    queryset = models.FinalSalaryNegotiationModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(assignedBy=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        jobApplication = UserJobAppliedModel.objects.get(id=serializer.data.get('jobApplication'))
        # print(jobApplication)
        jobStatus = jobApplication.jobPostId.jobProgressStatus.filter()
        # print(jobStatus.filter(status='Document Submission').get())
        jobApplication.jobProgressStatus = jobStatus.filter(status='Document Submission').get()
        jobApplication.save()

        # Email sending functionality
        try:
            job=jobApplication.jobPostId.jobTitle.capitalize()
            email_subject = f'{jobApplication.jobProgressStatus} | {job} | TechForing Career'
            email_body=render_to_string('emailTemplate/documentsubmission.html', 
                                                                {'applicant_name':jobApplication.userId.full_name,'job':job})
            data = {'email_body': email_body, 'to_email': jobApplication.userId.email,
                    'email_subject': email_subject}
            Util.send_email_body(data)
            return Response({'detail': 'Email Sent.'})
        except:
            return Response({'detail': 'Email Sending failed.'})

        # return Response(serializer.data)


"""
=======================Document section =======================
"""


class SelectedForDocumentView(generics.ListAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.SelectedForDocumentationSerializer

    def get_queryset(self):
        jobId = self.kwargs['job_id']
        search = self.request.query_params.get('search')
        # queryset = DocumentSubmissionModel.objects.filter(applied_job__jobPostId_id=jobId)
        queryset = UserJobAppliedModel.objects.filter(jobPostId_id=jobId,
                                                      jobProgressStatus__status='Document Submission')
        return queryset.filter(Q(userId__email__icontains=search) |
                               Q(userId__full_name__icontains=search) |
                               Q(jobPostId__jobTitle__icontains=search) |
                               Q(jobPostId__jobType__icontains=search)
                               )


# class DocumentRequestView(generics.RetrieveAPIView):
#     permission_classes = [customPermission.Authenticated]
#     serializer_class = serializer.DocumentRequestSerializer
#     queryset = UserJobAppliedModel.objects.all()
#     lookup_field = 'id'
#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer()
#         applicationData = UserJobAppliedModel.objects.get(id=self.kwargs['id'])
#         email_body = 'Hi ' + applicationData.userId.full_name + \
#                      f' you are selected for the Interview stage.' \
#                      'Prepare yourself.'
#
#         data = {'email_body': email_body, 'to_email': applicationData.userId.email,
#                 'email_subject': 'Status of the Screening Test'}
#         Util.send_email(data)
#         return Response(serializer.data)


class AdminDocumentVerificationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AdminDocumentVerificationSerializer

    def get_queryset(self):
        return DocumentSubmissionModel.objects.filter(applied_job=self.kwargs['applied_job'])

    def list(self, request, *args, **kwargs):
        applicationId = self.kwargs['applied_job']
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # print(serializer)
        responseData = serializer.data
        if len(responseData) > 0:
            # references = ReferenceInformationModel.objects.filter(applied_job=applicationId)
            jobApplication = UserJobAppliedModel.objects.get(id=applicationId)
            jobDetails = JobPostModel.objects.get(id=jobApplication.jobPostId.id)
            jobName = jobDetails.jobTitle
            progressStatus = jobApplication.jobProgressStatus.status
            # responseData.append({'references': references})
            responseData.append(
                {
                    'jobTitle': jobName,
                    'department': jobDetails.department.department,
                    'progressStatus': progressStatus,

                }
            )

            return Response(responseData)
        else:
            return Response({'detail': 'No documents found.'}, status=status.HTTP_404_NOT_FOUND)


class DocumentVerifiedView(generics.RetrieveUpdateAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.AdminDocumentVerifySerializer
    queryset = DocumentSubmissionModel.objects.all()
    lookup_field = 'applied_job'


class CommentsOnDocumentsView(generics.CreateAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.CommentsOnDocumentsSerializer
    queryset = models.CommentsOnDocumentsModel.objects.all()


class ReferenceVerificationView(generics.RetrieveUpdateAPIView):
    """
    Reference verification
    """
    permission_classes = [customPermission.Authenticated, customPermission.EmployeeAdminAuthenticated]
    serializer_class = serializer.ReferenceVerificationSerializer
    queryset = ReferenceInformationModel.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        ser = self.get_serializer(self.get_queryset())
        response = ser.data
        refId = self.kwargs['id']
        refInfo = ReferenceInformationModel.objects.get(id=refId)
        current_site = get_current_site(request).domain
        if current_site == 'careeradmin.techforing.com':
            site_link = 'career.techforing.com'
        else:
            site_link = 'devcareer.techforing.com'
        reference_verify_link = f'{site_link}/add_reference_form/{refInfo.slug_field}'

        email_body = render_to_string('emailTemplate/reference_verification.html',{
            'reference_verify_link': reference_verify_link,
            'applicant_name': refInfo.applied_job.userId.full_name,
        })

        data = {'email_body': email_body, 'to_email': refInfo.email,
                'email_subject': 'Reference Verification.'}
        Util.send_email_body(data)

        refInfo.is_sent = True
        refInfo.save()
        return Response(response)

    def update(self, request, *args, **kwargs):
        refId = self.kwargs['id']
        documents = DocumentSubmissionModel.objects.get(applied_job__references_submission_applied_job=refId)
        if documents.is_verified:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            refInfo = ReferenceInformationModel.objects.get(id=refId)
            refCheck = ReferenceInformationModel.objects.filter(applied_job=refInfo.applied_job)

            count = 0
            for ref in refCheck:
                if ref.is_verified:
                    count += 1

                if len(refCheck) == count:
                    refInfo.applied_job.jobProgressStatus = JobStatusModel.objects.get(status='On Boarding')
                    refInfo.applied_job.save()

                    email_body = f'Hi  {refInfo.applied_job.userId.full_name},\n We have verified your documents and ' \
                                 f'references. As you documents and references verification is completed, You are requested to ' \
                                 f'read our terms & conditions, if you are agree please submit you valuable feedback.\n\n' \
                                 'Thanks & Regards,\n' \
                                 'HR Department\n' \
                                 'TechForing Limited.\n' \
                                 'www.techforing.com'
                    # f'Office Address: House: 149 (4th floor), Lane: 1, Baridhara DOHS, Dhaka.\n' \

                    data = {'email_body': email_body, 'to_email': refInfo.applied_job.userId.email,
                            'email_subject': 'Update'}
                    Util.send_email(data)
            if refInfo.is_rejected:
                email_subject=f'Update Reference| TechForing Career'
                refName=refInfo.name
                email_body=render_to_string('emailTemplate/update_reference.html', 
                                {'ref_name':refName, 'applicant_name': refInfo.user.full_name})
                data = {'email_body': email_body, 'to_email': self.request.user.email,
                                'email_subject': email_subject}
                utils.Util.send_email_body(data)

        else:
            return Response({'message': 'Documents is not verified yet.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class SelectedForOnboardView(generics.ListAPIView):
    """
    selected for onboard  candidate list
    """
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.OnboardListSerializer

    def get_queryset(self):
        jobId = self.kwargs['job_id']
        search = self.request.query_params.get('search')
        # queryset = DocumentSubmissionModel.objects.filter(applied_job__jobPostId_id=jobId)
        queryset = UserJobAppliedModel.objects.filter(jobPostId_id=jobId,
                                                      jobProgressStatus__status='On Boarding',
                                                      userId__is_candidate=True)
        return queryset.filter(Q(userId__email__icontains=search) |
                               Q(userId__full_name__icontains=search) |
                               Q(jobPostId__jobTitle__icontains=search) |
                               Q(jobPostId__jobType__icontains=search)
                               )


class GenerateAppointmentLetterView(generics.CreateAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.GenerateAppointmentLetterSerializer
    queryset = models.GenerateAppointmentLetterModel.objects.all()

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


class AppointmentLetterInformationView(generics.ListCreateAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.GenerateAppointmentLetterSerializer

    def get_queryset(self):
        applicationId = self.kwargs['applied_job']
        queryset = UserJobAppliedModel.objects.filter(id=applicationId)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data
        applicationId = self.kwargs['applied_job']
        userInformation = UserJobAppliedModel.objects.get(id=applicationId)
        data = models.FinalSalaryNegotiationModel.objects.get(jobApplication=applicationId)
        grossSalary = int(data.finalSalary)
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
        # candidate and job information
        responseData.append({
            'applicantName': userInformation.userId.full_name,
            'location': userInformation.userId.location,
            'nid': userInformation.userId.nid,
            'phone': userInformation.userId.phone_number,
            'candidate_email': userInformation.userId.email,
            'exp_joining_data': userInformation.applied_job_user_applied_model.all().last().expectedJoiningData,
            # job info
            'jobTitle': userInformation.jobPostId.jobTitle,
            'jobType': userInformation.jobPostId.jobType,
            'job_responsibilities': userInformation.jobPostId.jobResponsibilities,
            # issued date
            'issued_date': userInformation.official_documents_application_id.get().issued_date
        })

        return Response(responseData)


class OfficialDocumentsView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [customPermission.Authenticated]
    serializer_class = serializer.OfficialDocumentsSerializer
    queryset = OfficialDocumentsModel.objects.all()
    lookup_field = 'applicationId'

    def perform_create(self, serializer):
        serializer.save(applicationId=UserJobAppliedModel.objects.get(id=self.kwargs['applicationId']))
        # try:
        #     redundant = OfficialDocumentsModel.objects.filter(applicationId=self.kwargs['applicationId'])
        #     if not redundant:
        #         serializer.save(applicationId=UserJobAppliedModel.objects.get(id=self.kwargs['applicationId']))
        # except AssertionError as ae:
        #     raise

    def create(self, request, *args, **kwargs):
        applicationId = self.kwargs['applicationId']
        alreadyCreated = OfficialDocumentsModel.objects.filter(applicationId=applicationId)
        # terms_condition = CandidateJoiningFeedbackModel.objects.filter(applicationId=applicationId).first()
        if alreadyCreated.count() < 1:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            email_body = f'Hi  {alreadyCreated.first().applicationId.userId.full_name},\n ' \
                         f'Congratulations, Your appointment letter is Updated to your portal.' \
                         f'please check you portal for further process.\n\n' \
                         'Thanks & Regards,\n' \
                         'HR Department\n' \
                         'TechForing Limited.\n' \
                         'www.techforing.com'
            # f'Office Address: House: 149 (4th floor), Lane: 1, Baridhara DOHS, Dhaka.\n' \

            data = {'email_body': email_body, 'to_email': alreadyCreated.first().applicationId.userId.email,
                    'email_subject': 'Update'}
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already created Appointment letter for this candidate.'},
                        status=status.HTTP_208_ALREADY_REPORTED)

        # if terms_condition is not None:
        #     if terms_condition.allowed:
        #         if alreadyCreated.count() < 1:
        #             serializer = self.get_serializer(data=request.data)
        #             serializer.is_valid(raise_exception=True)
        #             self.perform_create(serializer)
        #
        #             email_body = f'Hi  {alreadyCreated.first().applicationId.userId.full_name},\n Congratulations, Your appointment letter is Updated to your portal.' \
        #                          f'please check you portal for further process.\n\n' \
        #                          'Thanks & Regards,\n' \
        #                          'HR Department\n' \
        #                          'TechForing Limited.\n' \
        #                          'www.techforing.com'
        #             # f'Office Address: House: 149 (4th floor), Lane: 1, Baridhara DOHS, Dhaka.\n' \
        #
        #             data = {'email_body': email_body, 'to_email': alreadyCreated.first().applicationId.userId.email,
        #                     'email_subject': 'Update'}
        #             Util.send_email(data)
        #             return Response(serializer.data, status=status.HTTP_201_CREATED)
        #         return Response({'detail': 'Already created Appointment letter for this candidate.'},
        #                         status=status.HTTP_208_ALREADY_REPORTED)
        #
        #     return Response({'detail': 'This candidate is not agreed with our terms and conditions. Please talk with him and allow him to go further.'},
        #                     status=status.HTTP_403_FORBIDDEN)
        #
        # else:
        #     return Response({'detail': 'This candidate didn\'t provide feedback.'},
        #                     status=status.HTTP_400_BAD_REQUEST)
