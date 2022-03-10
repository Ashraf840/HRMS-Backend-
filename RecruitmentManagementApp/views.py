import base64
import datetime
from _testcapi import raise_exception
from django.db.models import Q
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from SupportApp import sms
from UserApp import utils
from UserApp.models import User
from UserApp.permissions import IsHrUser, EditPermission, IsAuthor, IsEmployee, IsCandidateUser, Authenticated, \
    EmployeeAdminAuthenticated
from . import models
from . import serializer


# For Admin to view all Users Information
class AllUserDetailView(generics.ListAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.AllUserDetailsSerializer
    queryset = User.objects.all()


# if user is HR then he/she can post a job
class JobPostView(generics.CreateAPIView):
    permission_classes = [Authenticated, IsHrUser]
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
    permission_classes = [Authenticated, IsHrUser]
    serializer_class = serializer.JobCreateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return models.JobPostModel.objects.filter(id=id)


# if User is Authenticated and IsCandidate then User can only apply
class AppliedForJobView(generics.CreateAPIView, generics.RetrieveAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.AppliedForJobSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_hr:
            queryset = models.UserJobAppliedModel.objects.all()
        else:
            queryset = models.UserJobAppliedModel.objects.filter(userId=self.request.user)
        return queryset

    lookup_field = 'jobPostId_id'

    def get(self, request, *args, **kwargs):
        try:
            checkApplication = models.UserJobAppliedModel.objects.filter(jobPostId=self.kwargs['jobPostId_id'],
                                                                         userId=self.request.user)
            if checkApplication.count() > 0:
                for application in checkApplication:
                    if application.jobProgressStatus.status != 'Withdrawn':
                        return Response({'detail': 'Already apply for this Position.'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        dayCount = application.appliedDate + datetime.timedelta(days=30)
                        today = datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=datetime.timedelta()))
                        if today < dayCount:
                            return Response(
                                {'detail': 'You have withdraw your application, you can apply again after 30 days.'},
                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response('Apply')

            return Response('Apply')
        except:
            data = self.get_serializer(self.get_queryset(), many=True)
            responseData = data.data
            return Response(responseData)

    def perform_create(self, serializer):
        jobId = serializer.validated_data['jobPostId']
        applicationData = models.UserJobAppliedModel.objects.filter(jobPostId=jobId, userId=self.request.user)

        serializer.save(userId=self.request.user,
                        jobProgressStatus=models.JobStatusModel.objects.get(status='new'))
        jobId = serializer.data['jobPostId']
        checkFilterQuestions = models.JobApplyFilterQuestionModel.objects.filter(jobId=jobId)
        if len(checkFilterQuestions) < 1:
            jobInfo = models.JobPostModel.objects.get(id=jobId).jobProgressStatus.all()
            if applicationData.count() > 1:
                for application in applicationData:
                    if application.jobProgressStatus.status.lower() == 'new':
                        jobApplication = applicationData.get()
                        break
            else:
                jobApplication = applicationData.get()

            for state in jobInfo:
                if state.status != 'new':
                    jobApplication.jobProgressStatus = state
                    jobApplication.save()
                    email_body = 'Hi ' + self.request.user.full_name + \
                                 f' Congratulations you have been selected for the {state.status} stage.' \
                                 'All the best in your job search!'

                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                            'email_subject': 'Status of the Screening Test'}
                    utils.Util.send_email(data)
                    break

        # jobId = serializer.validated_data['jobPostId']
        # applicationData = models.UserJobAppliedModel.objects.filter(jobPostId=jobId, userId=self.request.user)
        # # If application withdraw then they can apply again after 30 days.
        # if applicationData.count() >= 1:
        #     for application in applicationData:
        #         if application.jobProgressStatus.status == 'Withdraw':
        #             dayCount = application.appliedDate + datetime.timedelta(days=1)
        #             today = datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=datetime.timedelta()))
        #             if today > dayCount:
        #                 serializer.save(userId=self.request.user,
        #                                 jobProgressStatus=models.JobStatusModel.objects.get(status='new'))
        #                 jobId = serializer.data['jobPostId']
        #                 checkFilterQuestions = models.JobApplyFilterQuestionModel.objects.filter(jobId=jobId)
        #                 if len(checkFilterQuestions) < 1:
        #                     jobInfo = models.JobPostModel.objects.get(id=jobId).jobProgressStatus.all()
        #                     jobApplication = applicationData.get()
        #
        #                     for state in jobInfo:
        #                         if state.status != 'new':
        #                             jobApplication.jobProgressStatus = state
        #                             jobApplication.save()
        #                             email_body = 'Hi ' + self.request.user.full_name + \
        #                                          f' Congratulations you have been selected for the {state.status} stage.' \
        #                                          'All the best in your job search!'
        #
        #                             data = {'email_body': email_body, 'to_email': self.request.user.email,
        #                                     'email_subject': 'Status of the Screening Test'}
        #                             utils.Util.send_email(data)
        #                             break
        #             else:
        #                 return Response(
        #                     {'detail': 'You have withdraw your application, you can apply again after 30 days.'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        #
        #     return Response({'detail': 'Already Applied for this position.'}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     serializer.save(userId=self.request.user, jobProgressStatus=models.JobStatusModel.objects.get(status='new'))
        #     jobId = serializer.data['jobPostId']
        #     checkFilterQuestions = models.JobApplyFilterQuestionModel.objects.filter(jobId=jobId)
        #     if len(checkFilterQuestions) < 1:
        #         jobInfo = models.JobPostModel.objects.get(id=jobId).jobProgressStatus.all()
        #         jobApplication = applicationData.get()
        #
        #         for state in jobInfo:
        #             if state.status != 'new':
        #                 jobApplication.jobProgressStatus = state
        #                 jobApplication.save()
        #                 email_body = 'Hi ' + self.request.user.full_name + \
        #                              f' Congratulations you have been selected for the {state.status} stage.' \
        #                              'All the best in your job search!'
        #
        #                 data = {'email_body': email_body, 'to_email': self.request.user.email,
        #                         'email_subject': 'Status of the Screening Test'}
        #                 utils.Util.send_email(data)
        #                 break

    def create(self, request, *args, **kwargs):
        jobId = request.data['jobPostId']
        applicationData = models.UserJobAppliedModel.objects.filter(jobPostId=jobId, userId=self.request.user)
        # If application withdraw then they can apply again after 30 days.
        if applicationData.count() >= 1:
            for index, application in enumerate(applicationData):
                if applicationData.count() - 1 == index:
                    if application.jobProgressStatus.status == 'Withdrawn':
                        dayCount = application.appliedDate + datetime.timedelta(days=30)
                        today = datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=datetime.timedelta()))
                        if today > dayCount:
                            serializer = self.get_serializer(data=request.data)
                            serializer.is_valid(raise_exception=True)
                            self.perform_create(serializer)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response(
                                {'detail': 'You have withdraw your application, you can apply again after 30 days.'},
                                status=status.HTTP_400_BAD_REQUEST)

                return Response({'detail': 'Already Applied for this position.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    permission_classes = [Authenticated, IsAuthor, EditPermission]
    serializer_class = serializer.MyJobListSerializer

    def get_queryset(self):
        return models.UserJobAppliedModel.objects.filter(userId_id=self.request.user.id)


"""
Filter questions Sections
"""


class FilterQuestionListView(generics.ListAPIView):
    """
    filter question list with search field
    """
    permission_classes = [Authenticated, IsEmployee]
    serializer_class = serializer.FilterQuestionListSerializer

    def get_queryset(self):
        queryset = models.JobApplyFilterQuestionModel.objects.all()
        try:
            search = self.request.query_params.get('search')

            return queryset.filter(Q(jobId__jobTitle__icontains=search) |
                                   Q(question__icontains=search) |
                                   Q(fieldType__icontains=search))
        except:
            return queryset


class CandidateFilterQuestionListView(generics.ListAPIView):
    permission_classes = [Authenticated, IsCandidateUser]
    serializer_class = serializer.CandidateFilterQuestionListSerializer

    def get_queryset(self):
        jobId = self.kwargs['jobId']
        queryset = models.JobApplyFilterQuestionModel.objects.filter(jobId=jobId)
        return queryset


class FilterQuestionView(generics.ListCreateAPIView):
    permission_classes = [Authenticated, IsEmployee]
    serializer_class = serializer.FilterQuestionAnswerSerializer

    def get_queryset(self):
        return models.FilterQuestionAnswerModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FilterQuestionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.FilterQuestionAnswerSerializer
    queryset = models.FilterQuestionAnswerModel.objects.all()
    lookup_field = 'question_id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # print(instance)
            instance.question.delete()
            self.perform_destroy(instance)
        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Filter question response,
Filter question response List ,
Job searching,
Online test response,
practical test response
"""


class FilterQuestionResponseView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.FilterQuestionResponseSerializer
    queryset = models.FilterQuestionsResponseModelHR.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        reqData = request.data
        if type(reqData) == type([]):
            for job_list in request.data:
                jobId = job_list.get('jobPost')
                break
        else:
            jobId = request.data['jobPost']

        checkApplication = models.UserJobAppliedModel.objects.filter(userId=self.request.user, jobPostId_id=jobId)
        if len(checkApplication) >= 1:
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            for val in serializer.data:
                if val == 'id':
                    jobPostId = serializer.data['jobPost']
                    break
                else:
                    jobPostId = val['jobPost']
                    break

            filterQusResponse = models.FilterQuestionsResponseModelHR.objects.filter(user=self.request.user,
                                                                                     jobPost_id=jobPostId)

            jobFilterQuestion = models.UserJobAppliedModel.objects.get(jobPostId=jobPostId, userId=self.request.user)
            noOfQus = models.JobApplyFilterQuestionModel.objects.filter(jobId=jobPostId)

            totalQuestion = noOfQus.count()
            totalResponse = filterQusResponse.count()

            score = 0
            if totalResponse == totalQuestion:
                for res in filterQusResponse:
                    questionAnswer = models.FilterQuestionAnswerModel.objects.get(question=res.questions)

                    if questionAnswer.answer.lower() == res.response.lower():
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

                if totalQuestion - 1 <= score:
                    jobProgress = jobFilterQuestion.jobPostId.jobProgressStatus.all()
                    for i, progress in enumerate(jobProgress):

                        if jobFilterQuestion.jobProgressStatus.status == progress.status:
                            jobFilterQuestion.jobProgressStatus = models.JobStatusModel.objects.get(
                                status=jobProgress[i + 1].status)
                            jobFilterQuestion.save()
                            selectStatus = jobProgress[i + 1].status
                            # ========Email send functionality========

                            email_body = f'Dear {self.request.user.full_name},\n ' \
                                         f'Thank you for your application and interest in joining TechForing. You have been shortlisted for the {questionAnswer.question.jobId.jobTitle} position.\n' \
                                         f'At TechForing, we have a straightforward recruitment procedure and these {selectStatus} are one of them. We take these tests to understand your values, analytical ability, and expertise related to the position. This is a crucial and mandatory step to qualify for the position.\n' \
                                         f'You are requested to log into the recruitment portal and participate in the test. Link: https://career.techforing.com/\n' \
                                         f'NB: Follow the deadline and instructions strictly.\n' \
                                         f'Deadline: {datetime.date.today() + datetime.timedelta(hours=72)}\n\n\n' \
                                         f'Instructions:\n' \
                                         f'1. Use login credentials that you created when you applied.\n' \
                                         f'2. After completing the test, don’t forget to take the screenshot of your score.\n' \
                                         f'3. Upload your score and screenshots of your score as instructed.\n\n\n' \
                                         f'Thanks & Regards,\n' \
                                         f'HR Department\n' \
                                         f'TechForing Limited.\n' \
                                         f'www.techforing.com'

                            data = {'email_body': email_body, 'to_email': self.request.user.email,
                                    'email_subject': 'Screening Test result.'}
                            utils.Util.send_email(data)

                            """============SMS sending functionality============"""
                            msg = 'Hi ' + self.request.user.full_name + \
                                  f' Congratulations you have been selected for the {jobProgress[i + 1].status} stage.'
                            smsData = {'dest_num': self.request.user.phone_number, 'msg': msg}
                            sms.sendsms_response(smsData)

                            break
                else:
                    jobFilterQuestion.jobProgressStatus = models.JobStatusModel.objects.get(status='Rejected')
                    jobFilterQuestion.save()

                    email_body = f'Hi {self.request.user.full_name},\n ' \
                                 'We regret to inform you that we have decided to move forward with other candidates at ' \
                                 'this time. We will definitely keep you in mind for future opportunities that may be a ' \
                                 'good fit.' \
                                 'All the best in your job search!\n\n' \
                                 'Thanks & Regards,\n' \
                                 'HR Department\n' \
                                 'TechForing Limited.\n' \
                                 'www.techforing.com'

                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                            'email_subject': 'Status of the Screening Test'}

                    utils.Util.send_email(data)

                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response({'detail': 'new response added'})
        else:
            return Response({'detail': 'No application found'})


class FilterQuestionResponseListView(generics.ListAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.FilterQuestionResponseSerializer
    queryset = models.FilterQuestionsResponseModelHR.objects.all()


class PracticalTestView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.PracticalTestSerializer
    queryset = models.PracticalTestModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PracticalTestForApplicantView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.PracticalTestSerializer
    lookup_field = 'jobInfo'

    def get_queryset(self):
        queryset = models.PracticalTestModel.objects.filter(jobInfo_id=self.kwargs['jobInfo'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # file = serializer.validated_data.get('practicalFile')
        # link = serializer.validated_data.get('testLink')
        # if link == '' and file is None:
        #     # raise ValueError({'message': 'No file or link inserted.'})
        #     return Response({'message': 'Please insert a file or a test link.'})
        # else:
        #     serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data.get('practicalFile')
        link = serializer.validated_data.get('testLink')
        if link == '' and file is None:
            return Response({'error': 'Please insert a file or a test link.'})
        else:
            self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobCreateView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.JobCreateSerializer
    queryset = models.JobPostModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateCandidateStatusView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated, IsHrUser]
    serializer_class = serializer.CandidateStatusChangeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return models.UserJobAppliedModel.objects.filter(id=id)


class OnlineTestResponseListView(generics.ListAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.OnlineTestResponseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        id = self.kwargs['applied_job']
        return models.OnlineTestResponseModel.objects.filter(user=self.request.user,
                                                             appliedJob=models.UserJobAppliedModel.objects.get(
                                                                 id=id)).order_by('-id')

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        responseData = serializer.data

        id = self.kwargs['applied_job']
        jobPostId = models.UserJobAppliedModel.objects.get(id=id).jobPostId
        onlineTestLink = models.OnlineTestModel.objects.filter(jobInfo=jobPostId)

        if len(onlineTestLink) != 0:
            # data = models.OnlineTestResponseModel.objects.filter(user=self.request.user,
            #                                                      appliedJob=models.UserJobAppliedModel.objects.get(id=id))
            return Response(responseData)
        else:
            return Response({'detail': 'No data found.'},
                            status=status.HTTP_404_NOT_FOUND)


class OnlineTestResponseView(generics.CreateAPIView):
    """
    online test response view
    """
    permission_classes = [Authenticated]
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
                    jobApplication = models.UserJobAppliedModel.objects.get(id=applied_job)

                    onlineTestRes = models.OnlineTestResponseModel.objects.filter(user=self.request.user,
                                                                                  appliedJob=applied_job)
                    statusList = jobApplication.jobPostId.jobProgressStatus.all()
                    if onlineTestLink.count() == onlineTestRes.count():
                        for testMark in onlineTestRes:
                            if testMark.testMark < 50:
                                jobApplication.jobProgressStatus = models.JobStatusModel.objects.get(status='Rejected')
                                jobApplication.save()
                                email_body = f'Hi ' + self.request.user.full_name + \
                                             'We regret to inform you that we have decided to move forward with other candidates at ' \
                                             'this time. We will definitely keep you in mind for future opportunities that may be a ' \
                                             'good fit.' \
                                             'All the best in your job search!\n\n' \
                                             'Thanks & Regards,\n' \
                                             'HR Department\n' \
                                             'TechForing Limited.\n' \
                                             'www.techforing.com'

                                data = {'email_body': email_body, 'to_email': self.request.user.email,
                                        'email_subject': 'Status of the Screening Test'}
                                utils.Util.send_email(data)

                                return Response({'detail': 'sorry you are not selected for the next step'})
                        for i, sta in enumerate(statusList):
                            if sta.status == jobApplication.jobProgressStatus.status:
                                update = statusList[i + 1]
                                # print(update.status)
                                jobApplication.jobProgressStatus = models.JobStatusModel.objects.get(
                                    status=update.status)
                                jobApplication.save()
                                # email sending option
                                if update.status == 'F2F Interview':
                                    email_body = 'Hi ' + self.request.user.full_name + \
                                                 f'Congratulations! We are happy to inform you that you have passed the ' \
                                                 f'{sta.status} and have been selected for the second round of interview ' \
                                                 f'Go to our recruitment portal and follow the instruction\n' \
                                                 f'Thanks & Regards,\n' \
                                                 f'HR Department\n' \
                                                 f'TechForing Limited.\n' \
                                                 f'www.techforing.com'

                                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                                            'email_subject': f'Status of the {statusList[i]} Screening Test'}
                                    utils.Util.send_email(data)
                                else:

                                    email_body = f'Hi {self.request.user.full_name},\n' \
                                                 f'Congratulations! We are happy to inform you that you have passed ' \
                                                 f'the {sta.status} and have been selected for the second round of' \
                                                 f' interview which consists of a {update.status}.' \
                                                 f' Please read carefully and submit the task within the given' \
                                                 f' deadline. We expect you to carry out the task with full honesty. ' \
                                                 f'Follow the deadline and instructions easily.' \
                                                 f'Deadline: {datetime.date.today() + datetime.timedelta(hours=72)}\n\n' \
                                                 f'Go to our recruitment portal and follow the instruction\n' \
                                                 f'Thanks & Regards,\n' \
                                                 f'HR Department\n' \
                                                 f'TechForing Limited.\n' \
                                                 f'www.techforing.com'

                                    data = {'email_body': email_body, 'to_email': self.request.user.email,
                                            'email_subject': f'Status of the {statusList[i]} Screening Test'}
                                    utils.Util.send_email(data)
                                break
                        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                    return Response({'testName': serializer.data['testName'], 'testMark': serializer.data['testMark']})
                else:
                    return Response({'detail': 'You have already submitted online test Mark.'},
                                    status=status.HTTP_208_ALREADY_REPORTED)
            else:
                return Response({'detail': 'No test link found'},
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You are not allowed to attend online test.'},
                            status=status.HTTP_400_BAD_REQUEST)


class PracticalTestResponseView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.PracticalTestResponseSerializer
    queryset = models.PracticalTestResponseModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        appliedJob=models.UserJobAppliedModel.objects.get(id=self.kwargs['application_id']))

    def get(self, request, *args, **kwargs):
        check_redundancy = models.PracticalTestResponseModel.objects.filter(user=self.request.user,
                                                                            appliedJob=self.kwargs['application_id'])
        if len(check_redundancy) >= 1:
            return Response({'detail': 'You have already taken the test. Wait for review'})
        else:
            return Response([])

    def create(self, request, *args, **kwargs):
        applied_job = self.kwargs['application_id']
        # try:
        #
        # except:
        #     return Response({'detail': 'No Data found'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        try:
            check_redundancy = models.PracticalTestResponseModel.objects.get(user=self.request.user,
                                                                             appliedJob=applied_job)
            # print(check_redundancy)
            if check_redundancy is not None:
                return Response({'detail': 'You have already taken the test.'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            data = models.UserJobAppliedModel.objects.get(id=applied_job)
            if data.jobProgressStatus.status == 'Practical Test':
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'You can not attend this test.'}, status=status.HTTP_400_BAD_REQUEST)


"""
Document submission section during -> DocumentSubmissionView
User will upload during recruitment process -> ReferenceInformationView
"""


class DocumentSubmissionView(generics.CreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.DocumentationSubmissionSerializer
    queryset = models.DocumentSubmissionModel.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user,
                               applied_job=models.UserJobAppliedModel.objects.get(id=self.kwargs['job_id']))

    def create(self, request, *args, **kwargs):
        applied_job = self.kwargs['job_id']
        data = models.UserJobAppliedModel.objects.get(userId=self.request.user, id=applied_job)
        # print(data.jobProgressStatus.status)
        if data.jobProgressStatus.status == 'Document Submission':
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


class DocumentSubmissionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated, IsAuthor]
    serializer_class = serializer.DocumentationSubmissionSerializer
    # queryset = models.DocumentSubmissionModel.objects.all()
    lookup_field = 'applied_job'

    def get_queryset(self):
        applied_job = self.kwargs['applied_job']
        return models.DocumentSubmissionModel.objects.filter(applied_job=applied_job, user_id=self.request.user.id)


class ReferenceInformationView(generics.CreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.ReferenceInformationSerializer
    queryset = models.ReferenceInformationModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        applied_job=models.UserJobAppliedModel.objects.get(id=self.kwargs['application_id']))

    def create(self, request, *args, **kwargs):
        job_id = self.kwargs['application_id']
        documents = models.DocumentSubmissionModel.objects.filter(user=self.request.user,
                                                                  applied_job_id=job_id)

        if documents.exists():
            doc = documents.first()
            if doc.applied_job.jobProgressStatus.status == 'Document Submission':

                if type(request.data) == type([]):
                    for ref in request.data:
                        ref_email = ref.get('email')
                        domain_list = ["gmail.com", "yahoo.com", "hotmail.com", ]
                        domain = ref_email.split('@')[1]
                        official_email_count = 0
                        if domain in domain_list:
                            check_ref = models.ReferenceInformationModel.objects.filter(user=self.request.user,
                                                                                        applied_job_id=job_id)

                            for ref in check_ref:
                                if ref.email.split('@')[1] not in domain_list:
                                    official_email_count += 1
                        else:
                            official_email_count += 1
                    if official_email_count >= 1:
                        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                    else:
                        return Response({
                            'detail': "Please provide Official Email address like 'abc@techforing.com' of the referrer"},
                            status=status.HTTP_400_BAD_REQUEST)


                else:
                    ref_email = request.data.get('email')
                    domain_list = ["gmail.com", "yahoo.com", "hotmail.com", ]
                    domain = ref_email.split('@')[1]
                    if domain in domain_list:
                        check_ref = models.ReferenceInformationModel.objects.filter(user=self.request.user,
                                                                                    applied_job_id=job_id)
                        official_email_count = 0
                        for ref in check_ref:
                            if ref.email.split('@')[1] not in domain_list:
                                official_email_count += 1
                        if official_email_count >= 1:
                            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
                            serializer.is_valid(raise_exception=True)
                            self.perform_create(serializer)
                            headers = self.get_success_headers(serializer.data)
                            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                        else:
                            return Response({
                                'detail': "Please provide Official Email address like 'abc@techforing.com' of the referrer"},
                                status=status.HTTP_400_BAD_REQUEST)

                    else:
                        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


            else:
                return Response({'detail': 'You are not selected for Document verifications'},
                                status=status.HTTP_400_BAD_REQUEST)
            #
            # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            return Response({'detail': 'Document not Submitted Yet'},
                            status=status.HTTP_400_BAD_REQUEST)


class ReferenceInformationUpdateDeleteView(generics.ListAPIView):
    permission_classes = [Authenticated, IsAuthor]
    serializer_class = serializer.ReferenceInformationSerializer

    # lookup_field = 'applied_job'

    def get_queryset(self):
        applied_job = self.kwargs['applied_job']
        return models.ReferenceInformationModel.objects.filter(applied_job=applied_job, user_id=self.request.user.id)


# Signed appointment letter submission
class SignedAppointmentLetterSubmissionView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.SignedAppointmentLetterSerializer
    lookup_field = 'applicationId'

    def get_queryset(self):
        if self.request.user.is_hr or self.request.user.is_superuser:
            queryset = models.SignedAppointmentLetterModel.objects.all()
        else:
            queryset = models.SignedAppointmentLetterModel.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        applicationId=models.UserJobAppliedModel.objects.get(id=self.kwargs['applicationId']))

    def get(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_object())
        responseData = data.data
        if not responseData:
            return Response({'message': 'No Documents Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(responseData)

    def create(self, request, *args, **kwargs):
        applicationId = self.kwargs['applicationId']
        checkStatus = models.UserJobAppliedModel.objects.get(id=applicationId)
        if checkStatus.jobProgressStatus.status == 'On Boarding':
            try:
                checkDocuments = models.DocumentSubmissionModel.objects.get(Q(applied_job=applicationId),
                                                                            user=self.request.user)

                if checkDocuments.is_verified:
                    checkRef = models.ReferenceInformationModel.objects.filter(Q(applied_job=applicationId),
                                                                               user=self.request.user)
                    for ref in checkRef:
                        if not ref.is_verified:
                            return Response({'message': 'Your References is not verified yet.'},
                                            status=status.HTTP_400_BAD_REQUEST)

                    checkAppointment = models.OfficialDocumentsModel.objects.filter(applicationId=applicationId)
                    if checkAppointment.count() > 0:
                        checkSubmitted = models.SignedAppointmentLetterModel.objects.filter(
                            Q(applicationId=applicationId),
                            user=self.request.user)
                        if checkSubmitted.count() < 1:
                            ser = self.get_serializer(data=request.data)
                            ser.is_valid(raise_exception=True)
                            self.perform_create(ser)
                            return Response(ser.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response({'message': 'Already submitted.'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'message': 'Your Appointment letter is not ready yet.'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'Your Documents is not verified yet.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message': 'No Documents Found'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'You are not allowed to submit this documents.'},
                            status=status.HTTP_400_BAD_REQUEST)


# Withdraw job application
class WithdrawApplicationView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.CandidateStatusChangeSerializer
    queryset = models.UserJobAppliedModel.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        applicationData = models.UserJobAppliedModel.objects.get(id=self.kwargs['id'], userId=self.request.user)
        status = models.JobStatusModel.objects.all()
        applicationData.jobProgressStatus = status.get(status='Withdrawn')
        applicationData.save()
        """
        need to add Withdraw mail validation
        """
        return Response({'detail': 'Withdrawn'})


# Candidate Feedback about Hr policies
class CandidateJoiningFeedbackView(generics.ListCreateAPIView):
    permission_classes = [Authenticated]
    serializer_class = serializer.CandidateJoiningFeedbackSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_hr:
            queryset = models.CandidateJoiningFeedbackModel.objects.filter(applicationId=self.kwargs['application_id'])
        else:
            queryset = models.CandidateJoiningFeedbackModel.objects.filter(applicationId__userId=self.request.user)
        return queryset

    def perform_create(self, serializer):
        application_id = self.kwargs['application_id']
        serializer.save(applicationId=models.UserJobAppliedModel.objects.get(id=application_id))

    def get(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many=True)
        responseData = data.data
        if not responseData:
            return Response({'detail': 'no content'}, status=status.HTTP_404_NOT_FOUND)
        return Response(responseData)

    def create(self, request, *args, **kwargs):
        application_info = models.UserJobAppliedModel.objects.get(id=self.kwargs['application_id'])
        if application_info.jobProgressStatus.status == 'On Boarding':
            check_feedback = models.CandidateJoiningFeedbackModel.objects.filter(applicationId=application_info)
            if application_info.userId == self.request.user:
                if check_feedback.count() < 1:
                    ser = self.get_serializer(data=request.data)
                    ser.is_valid(raise_exception=True)
                    self.perform_create(ser)
                    check_value = models.CandidateJoiningFeedbackModel.objects.get(id=ser.data['id'])
                    if check_value.is_agree:
                        check_value.allowed = True
                        check_value.save()
                    else:
                        check_value.allowed = False
                        check_value.save()
                    responseData = ser.data
                    return Response(responseData, status=status.HTTP_201_CREATED)
                return Response(
                    {'detail': 'Already provide feedback, for further inquiries please contact on support.'},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'You dont have permission.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'You dont have permission to access this page'},
                            status=status.HTTP_400_BAD_REQUEST)


# Reference checking referee response functionality
class ReferenceQuestionsView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.ReferenceQuestionsSerializer
    permission_classes = [EmployeeAdminAuthenticated]
    queryset = models.ReferenceQuestionsModel.objects.all()
    lookup_field = 'id'


class ReferenceQuestionsRefView(generics.ListAPIView):
    serializer_class = serializer.ReferenceQuestionsSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.ReferenceQuestionsModel.objects.all()


class ReferenceInformationResponseView(generics.ListCreateAPIView):
    serializer_class = serializer.RefereeInformationSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.ReferenceResponseInformationView.objects.all()

