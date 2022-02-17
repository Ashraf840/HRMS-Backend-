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
        employee = self.request.user.employee_user_info.module_permission_employee
        if employee.is_superuser or employee.is_ceo or employee.is_gm or employee.is_hrm:
            queryset = hrm_models.EmployeeInformationModel.objects.filter(
                ~Q(user__email=self.request.user.email)).order_by('user__full_name')
        else:
            queryset = hrm_models.EmployeeInformationModel.objects.filter(
                ~Q(user__email=self.request.user.email),
                emp_department=self.request.user.employee_user_info.emp_department).order_by('user__full_name')
        # queryset = hrm_models.EmployeeInformationModel.objects.all()
        return queryset


class EmployeeEvaluationQuestionView(generics.ListAPIView):
    """
    1. Evaluation Questions and Possible Answers
    """
    serializer_class = hrm_serializers.EmployeeEvaluationQuestionSerializer
    permission_classes = [user_permissions.EmployeeAuthenticated]
    queryset = models.EmployeeCriteriaModel.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = models.EmployeeCriteriaModel.objects.all()
        # data = json.loads(serialize('json', queryset))
        data = hrm_serializers.EmployeeEvaluationQuestionSerializer(queryset, many=True)
        print(queryset.count())
        answers = []
        for x, y in models.ratings:
            answers.append({'id': x, 'criteria': y})
        return response.Response({
            'criteria': data.data,
            'answers': answers,
        })


class EmployeeEvaluationView(generics.ListCreateAPIView):
    """
    1. Employee Can Evaluate other Employees
    """
    serializer_class = hrm_serializers.EmployeeEvaluationSerializer
    permission_classes = [user_permissions.EmployeeAuthenticated]
    queryset = models.EmployeeEvaluationModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender_user=self.request.user, receiver_user=user_models.User.objects.get(id=self.kwargs['id']))

    def get(self, request, *args, **kwargs):
        current_month = datetime.today().month
        current_year = datetime.today().year
        current_user = self.request.user

        receiver_user = user_models.User.objects.get(id=self.kwargs['id'])

        criteria = models.EmployeeCriteriaModel.objects.all()
        evaluation = models.EmployeeEvaluationModel.objects.filter(sender_user=current_user,
                                                                   receiver_user=receiver_user,
                                                                   rating_date__month=current_month,
                                                                   rating_date__year=current_year)
        if criteria.count() <= evaluation.count():
            return response.Response({
                'message': 'Already Evaluated'
            })
        return response.Response('Create New')

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        current_month = datetime.today().month
        current_year = datetime.today().year
        current_user = self.request.user

        receiver_user = user_models.User.objects.get(id=self.kwargs['id'])
        current_criteria = (self.request.POST['criteria'])

        criteria = models.EmployeeCriteriaModel.objects.all()
        evaluation = models.EmployeeEvaluationModel.objects.filter(sender_user=current_user,
                                                                   receiver_user=receiver_user,
                                                                   rating_date__month=current_month,
                                                                   rating_date__year=current_year)

        if criteria.count() <= evaluation.count() or evaluation.filter(criteria__in=current_criteria):
            return response.Response({
                'message': 'Already Evaluated'
            })
        self.perform_create(ser)
        return response.Response(ser.data)
