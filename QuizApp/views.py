from rest_framework import generics, permissions
from UserApp.permissions import IsHrUser
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
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.SubmittedAnswerSerializer
    queryset = models.SubmittedAnswerModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubmittedAnswerListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.SubmittedAnswerListSerializer
    queryset = models.SubmittedAnswerModel.objects.all()


"""
Filter questions Sections
"""


class FilterQuestionView(generics.ListCreateAPIView):
    serializer_class = serializer.FilterQuestionSerializer
    # queryset = models.JobApplyFilterQuestionModel.objects.all()
    def get_queryset(self):
        try:
            id = self.kwargs['dep_id']
            return models.JobApplyFilterQuestionModel.objects.filter(department=id)
        except:
            return models.JobApplyFilterQuestionModel.objects.all()

# class FilterQuestionResponseView(generics.CreateAPIView):
#     serializer_class = serializer.FilterQuestionResponseSerializer
#     queryset = models.FilterQuestionsResponseModel.objects.all()
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class FilterQuestionResponseListView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializer.FilterQuestionResponseSerializer
#     queryset = models.FilterQuestionsResponseModel.objects.all()
