import requests
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, mixins, response, serializers, status
from HRM_controller import serializeres as hrm_serializers, models
from HRM_Admin import models as hrm_models
from HRM_User import models as hrm_user_models
from UserApp import permissions as user_permissions, models as user_models
from datetime import datetime, date, timedelta
from django.core.serializers import serialize
import json
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
            }, status=status.HTTP_400_BAD_REQUEST)
        data = json.loads(serialize('json', user_answer))
        # print(data[0])
        for d in data:
            d.pop('model')

        return response.Response(data)

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
                }, status=status.HTTP_400_BAD_REQUEST)

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
        # print(queryset.count())
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
    queryset = models.AttendanceShiftTimeModel.objects.all()
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
        print(posts.content.decode("utf-8"))
        all_employees = [item[0] for item in ast.literal_eval(posts.content.decode("utf-8").replace("u'", "'")
                                                              .replace('((', '(').replace('))', ')'))]
        print(all_employees)

        for employee in all_employees:
            models.AttendanceEmployeeRelModel.objects.get_or_create(registration_id=employee)
        employees = models.AttendanceEmployeeRelModel.objects.all()
        employee_list = []
        for emp in employees:
            try:
                employee_list.append({
                    'id': emp.id,
                    'employee': {
                        'employee_id': emp.employee.id,
                        'employee_name': emp.employee.user.full_name
                    },
                    'registration_id': emp.registration_id
                })
            except:
                employee_list.append({
                    'id': emp.id,
                    'employee': {
                        'employee_id': None,
                        'employee_name': None
                    },
                    'registration_id': emp.registration_id
                })
        return response.Response(employee_list)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        auth_user = 'Techforing_Ltd'
        auth_code = "09345jljrksdfhhsr745h3j4w8dd9fs"
        url = 'https://rumytechnologies.com/rams/json_api'

        data = {
            "operation": "delete_permanently",
            "auth_user": auth_user,
            "auth_code": auth_code,
            "username": instance.registration_id
        }

        posts = requests.post(url, json=data)
        if posts.content.decode("utf-8") == 'User Successfully Deleted':
            instance.delete()
            return response.Response({'message': 'Deleted Successfully'})

        return response.Response({'message': posts.content.decode("utf-8")}, status=status.HTTP_404_NOT_FOUND)


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


class EmployeeAttendanceLogView(generics.ListCreateAPIView):
    """
    Employee attendance log
    in/out time
    shift change hour count
    """
    permission_classes = [user_permissions.EmployeeAuthenticated]
    serializer_class = hrm_serializers.EmployeeAttendanceLogSerializer
    queryset = models.EmployeeAttendanceLogModel.objects.all()

    def data_convert(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    def time_convert(self, time):
        return datetime.strptime(time, '%H:%M:%S').time()

    def get(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many=True)
        responseData = data.data
        auth_user = 'Techforing_Ltd'
        auth_code = "09345jljrksdfhhsr745h3j4w8dd9fs"
        url = 'https://rumytechnologies.com/rams/json_api'
        start_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = start_date

        data = {
            "operation": "fetch_log",
            "auth_user": auth_user,
            "auth_code": auth_code,
            "start_date": start_date,
            "end_date": end_date
        }

        posts = requests.post(url, json=data)
        log_data = json.loads(posts.content.decode("utf-8"))
        for log in log_data.get('log'):
            employee_shift_rel = models.AttendanceEmployeeRelModel.objects.get_or_create(
                registration_id=log.get('registration_id'))[0]

            logs = log_data.get('log')
            try:
                # print(log['registration_id'])
                shift_start_time = employee_shift_rel.attendance_employee_relation.shift.shift_time.start_time
                if str(shift_start_time) > "16:00:00":

                    in_out_log = list(filter(
                        lambda l: l['registration_id'] == log['registration_id'], logs))
                    in_time = self.time_convert(in_out_log[-1]['access_time'])
                    in_date = self.data_convert(in_out_log[-1]['access_date'])
                    out_time = self.time_convert(in_out_log[0]['access_time'])
                    out_date = self.data_convert(in_out_log[0]['access_date'])

                    src = in_date - timedelta(days=1)
                    employee_log = models.EmployeeAttendanceLogModel.objects.get_or_create(employee=employee_shift_rel,
                                                                                           in_date=in_date,
                                                                                           in_time=in_time)
                    # try:
                    #     prv_day_log = models.EmployeeAttendanceLogModel.objects.get(employee=employee_shift_rel,
                    #                                                                 in_date=src)
                    #     # print(prv_day_log)
                    #     prv_day_log.out_time = out_time
                    #     prv_day_log.out_date = out_date
                    #     prv_day_log.save()
                    # except:
                    #     pass
                else:
                    in_out_log = list(filter(
                        lambda l: l['registration_id'] == log['registration_id'], logs))
                    print('else')
                    in_time = self.time_convert(in_out_log[0]['access_time'])
                    in_date = self.data_convert(in_out_log[0]['access_date'])
                    out_time = self.time_convert(in_out_log[-1]['access_time'])
                    out_date = self.data_convert(in_out_log[-1]['access_date'])
                    employee_log = models.EmployeeAttendanceLogModel.objects.get_or_create(employee=employee_shift_rel,
                                                                                           in_date=in_date,
                                                                                           in_time=in_time,
                                                                                           out_date=out_date,
                                                                                           out_time=out_time)
                    print(employee_log)

            except:
                in_out_log = list(filter(
                    lambda l: l['registration_id'] == log['registration_id'], logs))
                in_time = self.time_convert(in_out_log[-1]['access_time'])
                in_date = self.data_convert(in_out_log[-1]['access_date'])
                out_time = self.time_convert(in_out_log[0]['access_time'])
                out_date = self.data_convert(in_out_log[0]['access_date'])
                employee_log = models.EmployeeAttendanceLogModel.objects.get_or_create(employee=employee_shift_rel,
                                                                                       in_date=in_date,
                                                                                       in_time=in_time,
                                                                                       out_date=out_date,
                                                                                       out_time=out_time)
        return response.Response(log_data.get('log'))

class EmployeePromotionView(generics.ListCreateAPIView):
    """
    Employee promotion
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.EmployeePromotionSerializer
    queryset = models.EmployeePromotionModel.objects.all()
    
    #change the promote_to using the data from the serializer
    def perform_create(self, serializer):
        promote_to = serializer.validated_data.get('promotion_to')
        employee = serializer.validated_data.get('employee')
        employee.designation = promote_to
        employee.save()
        serializer.save()

#employee promotion update and delete view
class EmployeePromotionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Employee promotion update and delete
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.EmployeePromotionSerializer
    queryset = models.EmployeePromotionModel.objects.all()
    lookup_field = 'id'
class TerminationTitleView(generics.ListCreateAPIView):
    """
    Termination tile
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.TerminationTitleSerializer
    queryset = models.TerminationTitleModel.objects.all()

class TerminationTitleUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Termination tile update and delete
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.TerminationTitleSerializer
    queryset = models.TerminationTitleModel.objects.all()
    lookup_field = 'id'


class EmployeeTerminationView(generics.ListCreateAPIView):
    """
    Employee termination
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.EmployeeTerminationSerializer
    queryset = models.EmployeeTerminationModel.objects.all()

#employee termination update and delete view
class EmployeeTerminationUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Employee termination update and delete
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.EmployeeTerminationSerializer
    queryset = models.EmployeeTerminationModel.objects.all()
    lookup_field = 'id'
    
#employee resignation list view
class EmployeeResignationView(generics.ListAPIView):
    """
    Employee resignation
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.EmployeeResignationSerializer
    queryset = hrm_user_models.ResignationModel.objects.all()

class EmployeeResignationUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Employee resignation update and delete
    """
    permission_classes = [user_permissions.IsHrOrReadOnly]
    serializer_class = hrm_serializers.EmployeeResignationSerializer
    queryset = hrm_user_models.ResignationModel.objects.all()
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.resignatioAcceptDate=datetime.date(datetime.now())
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)