from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from UserApp.permissions import IsHrUser
from django.db.models import Q
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


class FilterQuestionListView(generics.ListAPIView):
    """
    filter question list with search field
    """
    serializer_class = serializer.FilterQuestionListSerializer

    def get_queryset(self):
        queryset = models.JobApplyFilterQuestionModel.objects.all()
        department = self.request.query_params.get('department')
        text_type = self.request.query_params.get('text_type')
        return queryset.filter(Q(department__department__icontains=department),
                               Q(fieldType__fieldType__icontains=text_type))


class FilterQuestionView(generics.ListCreateAPIView):
    serializer_class = serializer.FilterQuestionAnswerSerializer

    def get_queryset(self):
        try:
            id = self.kwargs['dep_id']
            return models.FilterQuestionAnswerModel.objects.filter(department=id)
        except:
            return models.FilterQuestionAnswerModel.objects.all()


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



    # def get_queryset(self):
    #     qus_id = self.kwargs['question_id']

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
