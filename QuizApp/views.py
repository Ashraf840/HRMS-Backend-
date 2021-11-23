from rest_framework import generics, permissions
from . import serializer
from . import models


# Create your views here.

# class QuestionSetView(generics.ListCreateAPIView):
#     serializer_class = serializer.QuestionSetSerializer
#     queryset = models.QuestionSetModel.objects.all()

class QuestionAnswerSetView(generics.ListCreateAPIView):
    serializer_class = serializer.QuestionAnswerSerializer
    queryset = models.QuestionAnswerModel.objects.all()


    # def perform_create(self, serializer):
    #     serializer.save(question__author = self.request.user)


class QuestionSetView(generics.ListCreateAPIView):
    serializer_class = serializer.QuestionSetSerializer
    queryset = models.QuestionSetModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
