from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, serializers, status, filters, views
from rest_framework.response import Response
from UserApp.models import User, JobPreferenceModel
from . import serializer
from UserApp.permissions import IsHrUser, IsCandidateUser, EditPermission
from . import models


# Create your views here.
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


# if User is Authenticated and IsCandidate then User can only apply
class AppliedForJobView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.AppliedForJobSerializer
    queryset = models.UserJobAppliedModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(userId=self.request.user, jobProgressStatus='new')


class JobDescriptionView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.JobPostSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return models.JobPostModel.objects.filter(id=id)


# GET data from Database
# If user applied ,user will see his job placement
class AppliedJobListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.AppliedForJobSerializer
    queryset = models.UserJobAppliedModel.objects.all()


# authenticated user can see all job post
class JobListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = serializer.JobPostSerializer
    queryset = models.JobPostModel.objects.all()


# class AppliedJobUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.UpdateAppliedJobSerializer
#     lookup_field = 'id'
#     queryset = models.UserJobAppliedModel.objects.all()
#     # def get_queryset(self):
#     #     u_id = self.kwargs['u_id']
#     #     id = self.kwargs['id']
#     #     return models.UserJobAppliedModel.objects.all()


class FilterQuestionResponseView(generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated, IsCandidateUser]
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


class JobDataFilterView(generics.ListAPIView):
    # queryset = models.JobPostModel.objects.all()
    serializer_class = serializer.JobPostSerializer

    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['jobTitle', 'department']
    # search_fields = ['$jobTitle', '$department']

    def get_queryset(self):
        queryset = models.JobPostModel.objects.all()
        # print(queryset)
        search = self.request.query_params.get('search')
        dep = self.request.query_params.get('department')
        # print(search)
        # print(dep)
        return queryset.filter(
            Q(jobTitle__icontains=search) |
            Q(department__department__icontains=search) |
            Q(level__icontains=search)
        )


class PracticalTestView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.PracticalTestSerializer
    queryset = models.PracticalTestModel.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class JobPostOnlineView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.OnlineTestSerializer
    queryset = models.OnlineTestModel.objects.all()


class OnlineTestResponseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.OnlineTestResponseSerializer
    queryset = models.OnlineTestResponseModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     response = models.OnlineTestResponseModel.objects.create(user_id=self.request.user.id,)


class PracticalTestResponseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.PracticalTestResponseSerializer
    queryset = models.PracticalTestModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
