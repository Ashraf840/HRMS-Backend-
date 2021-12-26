from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, serializers, status, filters, views
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from UserApp.models import User, JobPreferenceModel
from . import serializer
from UserApp.permissions import IsHrUser, IsCandidateUser, EditPermission, IsAuthor
from . import models


# For Admin to view all Users Information
class AllUserDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AllUserDetailsSerializer
    queryset = User.objects.all()


# if user is HR then he/she can post a job
class JobPostView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.JobPostSerializer
    queryset = models.JobPostModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobDescriptionView(generics.RetrieveAPIView):
    serializer_class = serializer.JobPostSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return models.JobPostModel.objects.filter(id=id)


# Update/delete functionality for admin
class JobDescriptionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.JobPostSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return models.JobPostModel.objects.filter(id=id)


# if User is Authenticated and IsCandidate then User can only apply
class AppliedForJobView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AppliedForJobSerializer
    queryset = models.UserJobAppliedModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(userId=self.request.user, jobProgressStatus=models.JobStatusModel.objects.get(status='new'))

    # def create(self, request, *args, **kwargs):
    #     try:


# GET data from Database
# If user applied ,user will see his job placement


# View job status
class JobStatusView(generics.ListAPIView):
    serializer_class = serializer.JobStatusSerializer
    queryset = models.JobStatusModel.objects.all()


# authenticated user can see all job post
class JobListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = serializer.JobPostSerializer
    queryset = models.JobPostModel.objects.all()


# Job searching Functionality
class JobDataFilterView(generics.ListAPIView):
    # queryset = models.JobPostModel.objects.all()
    serializer_class = serializer.JobPostSerializer

    def get_queryset(self):
        queryset = models.JobPostModel.objects.all()
        search = self.request.query_params.get('search')
        # dep = self.request.query_params.get('department')
        # print(search)
        # print(dep)
        return queryset.filter(
            Q(jobTitle__icontains=search) |
            Q(department__department__icontains=search) |
            Q(level__icontains=search) |
            Q(jobType__icontains=search)
        )


class MyJobListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthor, EditPermission]
    serializer_class = serializer.MyJobListSerializer

    def get_queryset(self):
        return models.UserJobAppliedModel.objects.filter(userId_id=self.request.user.id)


# class AppliedJobUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.UpdateAppliedJobSerializer
#     lookup_field = 'id'
#     queryset = models.UserJobAppliedModel.objects.all()
#     # def get_queryset(self):
#     #     u_id = self.kwargs['u_id']
#     #     id = self.kwargs['id']
#     #     return models.UserJobAppliedModel.objects.all()
"""
Filter question response,
Filter question response List ,
Job searching,
Online test response,
practical test response
"""


class FilterQuestionResponseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.FilterQuestionResponseSerializer
    queryset = models.FilterQuestionsResponseModelHR.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FilterQuestionResponseListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.FilterQuestionResponseSerializer
    queryset = models.FilterQuestionsResponseModelHR.objects.all()


class PracticalTestView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.PracticalTestSerializer
    queryset = models.PracticalTestModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PracticalTestForApplicantView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.PracticalTestSerializer
    lookup_field = 'jobInfo'

    def get_queryset(self):
        queryset = models.PracticalTestModel.objects.filter(jobInfo_id=self.kwargs['jobInfo'])
        return queryset


class JobPostOnlineView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.OnlineTestSerializer
    queryset = models.OnlineTestModel.objects.all()


class UpdateCandidateStatusView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.CandidateStatusChangeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        # data = models.UserJobAppliedModel.objects.get(id=id)
        # if not data.jobProgressStatus == 'rejected':
        #     if data.jobProgressStatus == 'new':
        #         data.jobProgressStatus = 'online'
        #     elif data.jobProgressStatus == 'online':
        #         data.jobProgressStatus = 'under_review'
        #     elif data.jobProgressStatus == 'under_review':
        #         data.jobProgressStatus = 'selected_for_practical'
        #     elif data.jobProgressStatus == 'selected_for_practical':
        #         data.jobProgressStatus = 'test_under_review'
        #     elif data.jobProgressStatus == 'test_under_review':
        #         data.jobProgressStatus = 'interview'
        #     elif data.jobProgressStatus == 'interview':
        #         data.jobProgressStatus = 'document'
        #     elif data.jobProgressStatus == 'document':
        #         data.jobProgressStatus = 'verification'
        #     elif data.jobProgressStatus == 'verification':
        #         data.jobProgressStatus = 'appointed'
        #
        #     else:
        #         data.jobProgressStatus = 'appointed'
        #
        #     data.save()
        return models.UserJobAppliedModel.objects.filter(id=id)


class OnlineTestResponseListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.OnlineTestResponseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        id = self.kwargs['applied_job']
        # onlineTestLink = models.OnlineTestModel.objects.filter(
        #     jobInfo=models.UserJobAppliedModel.objects.get(id=self.kwargs['applied_job']).id)

        return models.OnlineTestResponseModel.objects.filter(user=self.request.user, appliedJob=id)

    def list(self, request, *args, **kwargs):
        id = self.kwargs['applied_job']
        onlineTestLink = models.OnlineTestModel.objects.filter(
            jobInfo=models.UserJobAppliedModel.objects.get(id=self.kwargs['applied_job']).id)
        if len(onlineTestLink) != 0:
            data = models.OnlineTestResponseModel.objects.filter(user=self.request.user, appliedJob=id)
            return Response(data)
        else:
            return Response({'detail': 'No data'},
                            status=status.HTTP_204_NO_CONTENT)


class OnlineTestResponseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.OnlineTestResponseSerializer
    queryset = models.OnlineTestResponseModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        appliedJob=models.UserJobAppliedModel.objects.get(id=self.kwargs['applied_job']))

    def create(self, request, *args, **kwargs):
        applied_job = self.kwargs['applied_job']

        data = models.UserJobAppliedModel.objects.get(userId=self.request.user, id=applied_job)
        if data.jobProgressStatus.status == 'Online Test':
            onlineTestLink = models.OnlineTestModel.objects.filter(
                jobInfo=models.UserJobAppliedModel.objects.get(id=applied_job).id)
            print(models.UserJobAppliedModel.objects.get(id=applied_job).id)
            flag = len(onlineTestLink)
            # print(flag)
            if flag != 0:
                submittedData = models.OnlineTestResponseModel.objects.filter(user=self.request.user,
                                                                              appliedJob=applied_job)
                if len(submittedData) < flag:
                    serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))

                    # print(serializer)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response({'detail': 'You have already submitted online test Mark.'},
                                    status=status.HTTP_208_ALREADY_REPORTED)
            else:
                return Response({'detail': 'No test link found'},
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You are not allowed to attend online test.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({'detail': 'Wrong input details.'}, status=status.HTTP_404_NOT_FOUND)
        # try:
        #     try:
        #         check_redundancy = models.OnlineTestResponseModel.objects.get(user=self.request.user,
        #                                                                       appliedJob_id=job_id)
        #         if check_redundancy is not None:
        #             return Response({'detail': 'You have already taken the test.'}, status=status.HTTP_400_BAD_REQUEST)
        #     except:
        #         print('except')
        #         appliedJobData = models.UserJobAppliedModel.objects.get(userId=self.request.user, id=job_id)
        #         # print(appliedJobData.jobProgressStatus.status == 'online')
        #         if appliedJobData.jobProgressStatus.status == 'online':
        #             serializer = self.get_serializer(data=request.data)
        #             # print(serializer)
        #             serializer.is_valid(raise_exception=True)
        #             self.perform_create(serializer)
        #             headers = self.get_success_headers(serializer.data)
        #             appliedJobData.jobProgressStatus = models.JobStatusModel.objects.get(status='practical')
        #             appliedJobData.save()
        #             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #         else:
        #             return Response({'detail': 'You can not attend this test.'}, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({'detail': 'No Data found'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class PracticalTestResponseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.PracticalTestResponseSerializer
    queryset = models.PracticalTestResponseModel.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        appliedJob=models.UserJobAppliedModel.objects.get(id=self.kwargs['job_id']))

    def create(self, request, *args, **kwargs):
        applied_job = self.kwargs['job_id']
        try:
            try:
                check_redundancy = models.PracticalTestResponseModel.objects.get(user=self.request.user,
                                                                                 appliedJob=applied_job)

                if check_redundancy is not None:
                    return Response({'detail': 'You have already taken the test.'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                data = models.UserJobAppliedModel.objects.get(userId=self.request.user, id=applied_job)

                if data.jobProgressStatus.status == 'Practical Test':
                    serializer = self.get_serializer(data=request.data)
                    if serializer.is_valid():
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        # data.jobProgressStatus = models.JobStatusModel.objects.get(status='document')
                        # data.save()

                        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response({'detail': 'You can not attend this test.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail': 'No Data found'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
