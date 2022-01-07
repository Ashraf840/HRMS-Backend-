import datetime
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from UserApp.models import User
from QuizApp.models import FilterQuestionAnswerModel
from . import serializer
from UserApp.permissions import IsHrUser, EditPermission, IsAuthor
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
    """
    new job post will appear for candidate
    only active jobs will be visible for candidate site
    """
    permission_classes = []
    serializer_class = serializer.JobPostSerializer
    queryset = models.JobPostModel.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response = serializer.data
        data = self.get_queryset().filter(is_active=True)
        for job in data:
            # print(job.lastDateOfApply)
            if job.lastDateOfApply <= datetime.date.today():
                job.is_active = False
                job.save()
        return Response(response)


class JobDataFilterView(generics.ListAPIView):
    """
    Job searching Functionality
    """
    # queryset = models.JobPostModel.objects.all()
    serializer_class = serializer.JobPostSerializer

    def get_queryset(self):
        queryset = models.JobPostModel.objects.all()
        search = self.request.query_params.get('search')
        for job in queryset:
            if job.lastDateOfApply <= datetime.date.today():
                job.is_active = False
                job.save()
        # dep = self.request.query_params.get('department')
        # print(search)
        # print(dep)
        return queryset.filter(
            Q(jobTitle__icontains=search) |
            Q(department__department__icontains=search) |
            Q(level__icontains=search) |
            Q(jobType__icontains=search), is_active=True
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


class FilterQuestionResponseView(generics.ListCreateAPIView):
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
        filterQusResponse = models.FilterQuestionsResponseModelHR.objects.filter(
            appliedJob=serializer.data['appliedJob'])
        jobFilterQuestion = models.UserJobAppliedModel.objects.get(id=serializer.data['appliedJob'])
        totalQuestion = jobFilterQuestion.jobPostId.filterQuestions.count()

        score = 0
        for res in filterQusResponse:
            questionAnswer = FilterQuestionAnswerModel.objects.get(question=res.questions)
            if questionAnswer.answer == res.response:
                score += 1

            if not questionAnswer.answer == res.response:
                try:
                    resNum = int(res.response)
                    answer = int(questionAnswer.answer)
                    if 1000 < answer <= resNum:
                        score += 1
                    elif answer < 1000 and answer <= resNum:
                        score += 1
                except:
                    pass
        # print(score)
        jobProgress = jobFilterQuestion.jobPostId.jobProgressStatus.all()
        for i, progress in enumerate(jobProgress):
            if progress.status==jobFilterQuestion.jobProgressStatus.status:
                print('ok')
        if totalQuestion - 1 <= score:
            print(jobFilterQuestion.jobPostId.filterQuestions)
        else:
            print('rejected')

        # print(filterQusResponse)
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
    serializer_class = serializer.JobCreateSerializer
    queryset = models.OnlineTestModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateCandidateStatusView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.CandidateStatusChangeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserJobAppliedModel.objects.filter(id=id)


class OnlineTestResponseListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.OnlineTestResponseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        id = self.kwargs['applied_job']
        # onlineTestLink = models.OnlineTestModel.objects.filter(
        #     jobInfo=models.UserJobAppliedModel.objects.get(id=self.kwargs['applied_job']).id)
        # print(models.OnlineTestResponseModel.objects.filter(user=self.request.user,
        #                                                      appliedJob=models.UserJobAppliedModel.objects.get(
        #                                                          id=id)))
        return models.OnlineTestResponseModel.objects.filter(user=self.request.user,
                                                             appliedJob=models.UserJobAppliedModel.objects.get(
                                                                 id=id))

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data

        id = self.kwargs['applied_job']
        jobPostId = models.UserJobAppliedModel.objects.get(id=id).jobPostId
        onlineTestLink = models.OnlineTestModel.objects.filter(jobInfo=jobPostId)
        # print(len(onlineTestLink))
        if len(onlineTestLink) != 0:
            # data = models.OnlineTestResponseModel.objects.filter(user=self.request.user,
            #                                                      appliedJob=models.UserJobAppliedModel.objects.get(id=id))
            return Response(responseData)
        else:
            return Response({'detail': 'No Test link found.'},
                            status=status.HTTP_204_NO_CONTENT)


class OnlineTestResponseView(generics.CreateAPIView):
    """
    online test response view
    """
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
                jobInfo=models.UserJobAppliedModel.objects.get(id=applied_job).jobPostId)
            flag = len(onlineTestLink)
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
                print(check_redundancy)
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


"""
Document submission section during -> DocumentSubmissionView
User will upload during recruitment process -> ReferenceInformationView

"""


class DocumentSubmissionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.DocumentationSubmissionSerializer
    queryset = models.DocumentSubmissionModel.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user,
                               applied_job=models.UserJobAppliedModel.objects.get(id=self.kwargs['job_id']))

    def create(self, request, *args, **kwargs):
        applied_job = self.kwargs['job_id']
        data = models.UserJobAppliedModel.objects.get(userId=self.request.user, id=applied_job)
        # print(data.jobProgressStatus.status)
        if data.jobProgressStatus.status == 'Document':
            checkRedundancy = models.DocumentSubmissionModel.objects.filter(user=self.request.user,
                                                                            applied_job=applied_job)

            if checkRedundancy.exists():
                return Response({'detail': 'Your data has been updated already.'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': 'You are not selected for Document Submission'},
                            status=status.HTTP_403_FORBIDDEN)
            # more validation will be a plus.

        # try:

        # except:
        #     return Response({'detail': ''}, status=status.HTTP_400_BAD_REQUEST)


class DocumentSubmissionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    serializer_class = serializer.DocumentationSubmissionSerializer
    # queryset = models.DocumentSubmissionModel.objects.all()
    lookup_field = 'applied_job'

    def get_queryset(self):
        applied_job = self.kwargs['applied_job']
        return models.DocumentSubmissionModel.objects.filter(applied_job=applied_job, user_id=self.request.user.id)


class ReferenceInformationView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.ReferenceInformationSerializer
    queryset = models.ReferenceInformationModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        applied_job=models.UserJobAppliedModel.objects.get(id=self.kwargs['job_id']))

    def create(self, request, *args, **kwargs):
        job_id = self.kwargs['job_id']
        documents = models.DocumentSubmissionModel.objects.get(user=self.request.user,
                                                               applied_job_id=job_id)

        if documents.is_verified:
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            # print(serializer)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            print('save')
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': 'Document not Verified Yet'},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class ReferenceInformationUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    serializer_class = serializer.ReferenceInformationSerializer

    lookup_field = 'applied_job'

    def get_queryset(self):
        applied_job = self.kwargs['applied_job']
        return models.ReferenceInformationModel.objects.filter(applied_job=applied_job, user_id=self.request.user.id)
