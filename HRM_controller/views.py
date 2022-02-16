from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, mixins, response, serializers
from HRM_controller import serializeres as hrm_serializers, models
from UserApp import permissions as user_permissions, models as user_models
from datetime import datetime, date
from django.core.serializers import serialize
import json
from HRM_Admin import models as hrm_models


# Create your views here.
# Survey Section
class SurveyQuestionView(generics.ListCreateAPIView):
    """
    1. View for checking if user already submitted current months survey or not
    2. View for rendering list of questions and options
    """
    serializer_class = hrm_serializers.SurveyQuestionSerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]
    queryset = models.SurveyQuestionModel.objects.all()

    def get(self, request, *args, **kwargs):
        current_month = datetime.today().month
        current_year = datetime.today().year
        current_user = self.request.user
        user_answer = models.SurveyUserResponseModel.objects.filter(user=current_user, ans_time__month=current_month,
                                                                    ans_time__year=current_year)
        questions = models.SurveyQuestionModel.objects.all()

        if questions.count() == user_answer.count():
            return response.Response({
                'message': 'You have already submitted survey this month.'
            })
        data = hrm_serializers.SurveyQuestionSerializer(questions, many=True)

        return response.Response({'data': data.data})


class SurveyUserResponseView(generics.ListCreateAPIView):
    """
    1. View for User to submit their monthly survey
    """
    serializer_class = hrm_serializers.SurveyUserResponseSerializer
    permission_classes = [user_permissions.EmployeeAuthenticated]
    queryset = models.SurveyUserResponseModel.objects.all()

    # def get_queryset(self):
    #     current_month = datetime.today().strftime("%b")
    #     user_answer = models.SurveyUserResponseModel.objects.filter(months__iexact=current_month)
    #     return user_answer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_answered=True)

    def get(self, request, *args, **kwargs):
        current_month = datetime.today().month
        current_year = datetime.today().year
        current_user = self.request.user
        user_answer = models.SurveyUserResponseModel.objects.filter(user=current_user, ans_time__month=current_month,
                                                                    ans_time__year=current_year)
        questions_count = models.SurveyQuestionModel.objects.all().count()

        if questions_count == user_answer.count():
            return response.Response({
                'message': 'You have already submitted survey this month.'
            })
        data = json.loads(serialize('json', user_answer))

        return response.Response({
            'data': data
        })


# Employee Evaluation Section
class AllColleaguesView(generics.ListAPIView):
    """
    1. View Colleagues Information
    """
    permission_classes = [user_permissions.EmployeeAuthenticated]
    serializer_class = hrm_serializers.AllColleaguesSerializer
    # queryset = user_models.User.objects.all()
    filterset_fields = ['emp_department']

    def get_queryset(self):
        # if self.request.user.is
        queryset = hrm_models.EmployeeInformationModel.objects.filter(~Q(user__email=self.request.user.email)).order_by('user__full_name')
        # queryset = hrm_models.EmployeeInformationModel.objects.all()
        return queryset
