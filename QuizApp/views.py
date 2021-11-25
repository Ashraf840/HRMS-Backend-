from rest_framework import generics, permissions
from UserApp.permissions import IsHrUser, IsCandidateUser, EditPermission
from . import serializer
from . import models


# Create your views here.

# class QuestionSetView(generics.ListCreateAPIView):
#     serializer_class = serializer.QuestionSetSerializer
#     queryset = models.QuestionSetModel.objects.all()

class QuestionAnswerSetView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.QuestionAnswerSerializer
    queryset = models.QuestionAnswerModel.objects.all()


class SubmittedAnswerView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidateUser,EditPermission]
    serializer_class = serializer.SubmitterAnswerSerializer
    queryset = models.SubmittedAnswerModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShowSubmittedAnswerView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, IsHrUser]
    serializer_class = serializer.SubmitterAnswerSerializer
    queryset = models.SubmittedAnswerModel.objects.all()

# class QuestionSetView(generics.ListCreateAPIView):
#     serializer_class = serializer.QuestionSetSerializer
#     queryset = models.QuestionSetModel.objects.all()
#
#     """
#     selecting the request user as author user
#     """
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
