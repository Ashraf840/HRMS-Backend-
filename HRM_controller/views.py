import requests
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, mixins, response, serializers
from HRM_controller import serializeres as hrm_serializers, models
from UserApp import permissions as user_permissions, models as user_models
from datetime import datetime, date
from django.core.serializers import serialize
import json
from HRM_Admin import models as hrm_models
import ast
from bs4 import BeautifulSoup
import requests


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
        answer_list = []
        ans_queryset = models.SurveyAnswerSheetModel.objects.all()
        for ans in ans_queryset:
            answer_list.append({
                'id': ans.id,
                'answer': ans.answers
            })

        data = hrm_serializers.SurveyQuestionSerializer(questions, many=True)

        return response.Response({'data': data.data, 'answers': answer_list})


class SurveyUserResponseView(generics.ListCreateAPIView):
    """
    1. View for User to submit their monthly survey
    """
    serializer_class = hrm_serializers.SurveyUserResponseSerializer
    permission_classes = [user_permissions.EmployeeAuthenticated]
    queryset = models.SurveyUserResponseModel.objects.all()

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

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        ser.is_valid(raise_exception=True)
        current_month = datetime.today().month
        current_year = datetime.today().year
        current_user = self.request.user
        for item in request.data:
            current_question = (item['question'])

            questions_count = models.SurveyQuestionModel.objects.all()
            user_answer = models.SurveyUserResponseModel.objects.filter(user=current_user,
                                                                        ans_time__month=current_month,
                                                                        ans_time__year=current_year)

            if (questions_count.count() <= user_answer.count()) or user_answer.filter(question_id=current_question):
                return response.Response({
                    'message': 'Already Evaluated'
                })

        self.perform_create(ser)
        return response.Response({
            'message': 'Evaluated'
        })


class SurveyDataView(generics.ListAPIView):
    """
    1. View for Users monthly survey data
    """
    serializer_class = hrm_serializers.SurveyDataSerializer


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
        try:
            employee = self.request.user.employee_user_info.module_permission_employee
            if employee.is_superuser or employee.is_ceo or employee.is_gm or employee.is_hrm:
                queryset = hrm_models.EmployeeInformationModel.objects.filter(
                    ~Q(user__email=self.request.user.email)).order_by('user__full_name')
            else:
                queryset = hrm_models.EmployeeInformationModel.objects.filter(
                    ~Q(user__email=self.request.user.email),
                    emp_department=self.request.user.employee_user_info.emp_department).order_by('user__full_name')

        except:
            queryset = hrm_models.EmployeeInformationModel.objects.filter(
                ~Q(user__email=self.request.user.email)).order_by('user__full_name')
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
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        ser.is_valid(raise_exception=True)

        current_month = datetime.today().month
        current_year = datetime.today().year
        current_user = self.request.user

        receiver_user = user_models.User.objects.get(id=self.kwargs['id'])
        for item in request.data:
            current_criteria = (item['criteria'])

            criteria = models.EmployeeCriteriaModel.objects.all()
            evaluation = models.EmployeeEvaluationModel.objects.filter(sender_user=current_user,
                                                                       receiver_user=receiver_user,
                                                                       rating_date__month=current_month,
                                                                       rating_date__year=current_year)

            if (criteria.count() <= evaluation.count()) or evaluation.filter(criteria_id=current_criteria):
                return response.Response({
                    'message': 'Already Evaluated'
                })
        self.perform_create(ser)
        return response.Response({
            'message': 'Evaluated'
        })


# Announcement, Notice and Complain Section
class AnnouncementView(generics.ListCreateAPIView):
    """
    1. Section for creating announcement
    2. Admin, HR, GM and CEO can create new announcement as well as view all announcements
    3. Other employees can only view announcements related to their department
    """
    serializer_class = hrm_serializers.AnnouncementSerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]
    queryset = models.AnnouncementModel.objects.all()

    def get_queryset(self):
        try:
            employee = self.request.user.employee_user_info.module_permission_employee
            if employee.is_superuser or employee.is_ceo or employee.is_gm or employee.is_hrm:
                queryset = models.AnnouncementModel.objects.all()
            else:
                queryset = models.AnnouncementModel.objects.filter(
                    department__in=[self.request.user.employee_user_info.emp_department])
        except:
            queryset = models.AnnouncementModel.objects.all()
        return queryset


class NoticeView(generics.ListCreateAPIView):
    """
    1. Section for creating notice
    2. Admin, HR, GM and CEO can create new notice as well as view all notices
    3. Other employees can only view notices related to their department
    """
    serializer_class = hrm_serializers.NoticeSerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]

    def get_queryset(self):
        try:
            employee = self.request.user.employee_user_info.module_permission_employee
            if employee.is_superuser or employee.is_ceo or employee.is_gm or employee.is_hrm:
                queryset = models.NoticeModel.objects.all()
            else:
                queryset = models.NoticeModel.objects.filter(
                    department__in=[self.request.user.employee_user_info.emp_department])
        except:
            queryset = models.NoticeModel.objects.all()
        return queryset


class ComplainView(generics.ListCreateAPIView):
    serializer_class = hrm_serializers.ComplainSerializer
    permission_classes = [user_permissions.EmployeeAuthenticated]
    queryset = models.ComplainModel.objects.all()


class ComplainResolvedView(generics.RetrieveUpdateAPIView):
    serializer_class = hrm_serializers.ComplainResolvedSerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]
    queryset = models.ComplainModel.objects.all()
    lookup_field = 'id'


# Attendance Section
class AttendanceShiftView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    """
    1. Manager can create employee shift
    2. Manager can update shift time
    """
    serializer_class = hrm_serializers.AttendanceShiftSerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]
    queryset = models.AttendanceEmployeeShiftModel.objects.all()
    lookup_field = 'id'


class AttendanceRegistrationView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    1. This api suppose to register user data from access controller
    2. Currently it only gets the existing data from access controller
    3. Can not create new data because of problem in access controller api
    """
    serializer_class = hrm_serializers.AttendanceRegistrationSerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]
    queryset = models.AttendanceEmployeeRelModel.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        auth_user = 'Techforing_Ltd'
        auth_code = "09345jljrksdfhhsr745h3j4w8dd9fs"
        url = 'https://rumytechnologies.com/rams/json_api'

        data = {
            "operation": "fetch_user_in_device_list",
            "auth_user": auth_user,
            "auth_code": auth_code,
        }

        posts = requests.post(url, json=data)

        all_employees = [item[0] for item in ast.literal_eval(posts.content.decode("utf-8").replace("u'", "'")
                                                              .replace('((', '(').replace('))', ')'))]
        for employee in all_employees:
            models.AttendanceEmployeeRelModel.objects.get_or_create(registration_id=employee)
        employees = models.AttendanceEmployeeRelModel.objects.all()
        employee_list = []
        for emp in employees:
            try:
                employee_list.append({
                    'id': emp.employee.id,
                    'employee_name': emp.employee.user.full_name,
                    'registration_id': emp.registration_id
                })
            except:
                employee_list.append({
                    'id': None,
                    'employee_name': None,
                    'registration_id': emp.registration_id
                })
        return response.Response(employee_list)


class CreateHolidaysView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    """
    1. Scrap Holiday list from Internet (Example: https://www.officeholidays.com/countries/bangladesh/2022)
    2. Update existing holiday
    3. Create new holiday
    """
    serializer_class = hrm_serializers.CreateHolidaySerializer
    permission_classes = [user_permissions.IsHrOrReadOnly]
    queryset = models.HolidayModel.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        # year = datetime.now().year
        # url = f'https://www.officeholidays.com/countries/bangladesh/{year}'
        #
        # ### Web Scraping ###
        # full_page = requests.get(url)
        # full_page = full_page.content
        # soup = BeautifulSoup(full_page, "html.parser")
        #
        # holidays = soup.find_all('tr', {'class': ['country', 'govt']})
        #
        # total_holidays = []
        # for holiday in holidays:
        #     day = holiday.find_all('td')[2].find('a').text
        #     h_date = holiday.find_all('td')[1].find('time')['datetime']
        #     models.HolidayModel.objects.get_or_create(holiday_name=day, holiday_date=h_date)

        # ls = [day, h_date]
        # total_holidays.append(ls)

        queryset = models.HolidayModel.objects.all()
        return queryset
