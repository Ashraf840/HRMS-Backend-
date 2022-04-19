import datetime
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status
from HRM_Admin import models as hrm_admin_model, serializer as hrm_admin_serializer
from HRM_User import models as hrm_user_models
from RecruitmentManagementApp import models as recruitment_model
from UserApp import models as user_model, permissions as custom_permission, utils
from AdminOperationApp import models as admin_operation_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from datetime import datetime

# email formatting library file
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


# Create your views here.
class EmployeeForDeptHeadView(generics.ListAPIView):
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeForDeptHeadSerializer

    def get_queryset(self):
        queryset = user_model.User.objects.filter(is_employee=True)
        return queryset


class OnboardAnEmployeeView(generics.ListCreateAPIView):
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = hrm_admin_serializer.OnboardNewEmployeeSerializer
    queryset = hrm_admin_model.EmployeeSalaryModel.objects.all()

    def create(self, request, *args, **kwargs):
        if type(request.data) == (type({})):
            user_id = request.data['employee'].get('user')
            designation_id = request.data['employee'].get('designation')
        else:
            user_id = request.data.get('employee.user')
            designation_id = request.data.get('employee.designation')

        checkDesignation = user_model.UserDesignationModel.objects.get(id=designation_id)
        userInfo = user_model.User.objects.get(id=user_id)
        # personal email will be stored here.
        user_personal_email = userInfo.email
        # user_email = userInfo.email
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if checkDesignation.designation != 'CEO':
            self.perform_create(serializer)
            if checkDesignation.designation == 'HR':
                userInfo.is_hr = True
        else:
            if userInfo.is_superuser:
                # finalSalary = admin_operation_model.FinalSalaryNegotiationModel.objects.get(
                #     jobApplication__userId__id=userInfo.id)
                self.perform_create(serializer)
            else:
                return Response({'message': 'You are not superuser'})

        userInfo.is_candidate = False
        userInfo.is_employee = True
        userInfo.email_validated = False
        try:
            userInfo.email = request.data['employee'].get('email')
        except:
            userInfo.email = request.data.get('employee.email')
        userInfo.save()

        # update personal email
        employee_info = hrm_admin_model.EmployeeInformationModel.objects.get(user=userInfo)
        employee_info.personal_email = user_personal_email
        employee_info.save()

        # Email activation email.
        token = RefreshToken.for_user(userInfo).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('tfhrm_api:employee-email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        email_body = f'Hi {userInfo.full_name},\n' \
                     f'Congratulation you profile has been updated. Now you can login as employee at "*hrms.techforing.com*" Please verify email and login into hrm site.\n' \
                     f'Official Email: {userInfo.email}\n' \
                     f'Password: Use you previous password, you have created during account creation.\n' \
                     f'If you forgot your password please verify your account and reset your password. and login into- hrms.techforing.com' \
                     f'Verification link {absurl}'

        # send mail on personal email
        data = {'email_body': email_body, 'to_email': user_personal_email,
                'email_subject': 'TechForing|Employee Verification Email'}

        data2 = {'email_body': email_body, 'to_email': userInfo.email,
                 'email_subject': 'TechForing|Employee Verification Email'}
        utils.Util.send_email(data)
        utils.Util.send_email(data2)
        return Response({'message': 'Employee added successfully'})


class AddEmployeeInfoView(generics.CreateAPIView):
    """
    Add new employee from admin panel,
    """
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = hrm_admin_serializer.SalaryInfoSerializer
    queryset = hrm_admin_model.EmployeeSalaryModel

    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        employee = user_data['employee']
        user = user_model.User.objects.get(email=employee['user'].get('email'))
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('tfhrm_api:employee-email-verify')
        absurl = 'http://' + current_site + "?token=" + str(token)

        email_body = f'Hi {user.full_name},\n' \
                     f'Congratulation You are officially appointed.To login please verify your account' \
                     f'Verification link {absurl}'

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verification Email'}

        utils.Util.send_email(data)
        return Response(user_data)

    # def create(self, request, *args, **kwargs):
    #     checkDesignation = user_model.UserDesignationModel.objects.get(id=request.data['employee.designation'])
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     userInfo = user_model.User.objects.get(id=request.data['employee.user'])
    #
    #     if checkDesignation.designation != 'CEO':
    #         self.perform_create(serializer)
    #         if checkDesignation.designation == 'HR':
    #             userInfo.is_hr = True
    #     else:
    #         if userInfo.is_superuser:
    #             # finalSalary = admin_operation_model.FinalSalaryNegotiationModel.objects.get(
    #             #     jobApplication__userId__id=userInfo.id)
    #             self.perform_create(serializer)
    #         else:
    #             return Response({'message': 'You are not superuser'})
    #
    #     userInfo.is_candidate = False
    #     userInfo.is_employee = True
    #     userInfo.email_validated = False
    #     userInfo.email = request.data['employee.email']
    #     userInfo.save()
    #
    #     # Email activation email.
    #     token = RefreshToken.for_user(userInfo).access_token
    #     current_site = get_current_site(request).domain
    #     relativeLink = reverse('tfhrm_api:employee-email-verify')
    #     absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
    #
    #     email_body = f'Hi {userInfo.full_name},\n' \
    #                  f'Congratulation you profile has been updated. Please verify email and login into hrm site.' \
    #                  f'Verification link {absurl}'
    #
    #     # html_message = render_to_string('html.html', context={})
    #     # plain_message = strip_tags(html_message)
    #     # email = EmailMultiAlternatives(
    #     #     'subject',
    #     #     plain_message,
    #     #     'pranto.techforing@gmail.com',
    #     #     ['zulkar.techforing@gmail.com']
    #     # )
    #     # email.attach_alternative(html_message,'text/html')
    #     # email.send()
    #     # email_body = plain_message
    #
    #     data = {'email_body': email_body, 'to_email': userInfo.email,
    #             'email_subject': 'Verification Email'}
    #
    #     utils.Util.send_email(data)
    #     return Response({'message': 'Employee added successfully'})


class EmployeeInformationListView(generics.ListAPIView):
    """
    All Employee List
    """
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeInformationListSerializer

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            queryset = hrm_admin_model.EmployeeInformationModel.objects.all()
            return queryset.filter(Q(user__full_name__icontains=search) |
                                   Q(emp_department__department__icontains=search) |
                                   Q(designation__designation__icontains=search) |
                                   Q(user__email__icontains=search))
        except:
            return hrm_admin_model.EmployeeInformationModel.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # print(serializer.data)
        serializerData = serializer.data
        allUser = hrm_admin_model.EmployeeInformationModel.objects.filter()
        totalEmployee = allUser.count()
        maleEmployee = allUser.filter(user__gender='Male').count()
        femaleEmployee = allUser.filter(user__gender='Female').count()
        today = datetime.date.today()
        prvDay = today - datetime.timedelta(days=30)
        newEmployee = hrm_admin_model.EmployeeInformationModel.objects.filter(
            joining_date__range=[prvDay, today]).count()

        responseData = {
            'employeeInfo': serializerData,
            'gender': {
                'total': totalEmployee,
                'male': maleEmployee,
                'female': femaleEmployee,
                'new_employee': newEmployee
            }
        }
        return Response(responseData)


class EmployeeInformationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeUpdateDeleteSerializer
    queryset = hrm_admin_model.EmployeeInformationModel.objects.all()
    lookup_field = 'user_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if type(request.data) == type({}):
            req_email = request.data['user'].get('email')
        else:
            print(type(request.data))
            req_email = request.data.get('user.email')
        if instance.user.email != req_email:
            email_validator = user_model.User.objects.filter(email=req_email)
            if len(email_validator) > 0:
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class EmployeeInformationView(generics.ListAPIView):
    """
    Employee information detailed view
    """
    permission_classes = [custom_permission.Authenticated]
    serializer_class = hrm_admin_serializer.EmployeeInformationSerializer

    def get_queryset(self):
        if self.request.user.is_hr or self.request.user.is_superuser:
            queryset = user_model.User.objects.filter(id=self.kwargs['user_id'], is_employee=True)
        else:
            queryset = user_model.User.objects.filter(id=self.request.user.id)
        return queryset


class EmployeeBankInformationView(generics.CreateAPIView):
    """
    Employee bank information add
    """
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeBankInformationSerializer
    queryset = hrm_admin_model.EmployeeBankInfoModel.objects.all()


class EmployeeBankInformationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Employee bank information update delete
    """
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeBankInformationSerializer
    queryset = hrm_admin_model.EmployeeBankInfoModel.objects.all()
    lookup_field = 'id'


class EmployeeDocumentsListView(generics.RetrieveAPIView):
    """
    Employee all documents
    """
    permission_classes = [custom_permission.CandidateAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeDocumentsSerializer
    queryset = recruitment_model.DocumentSubmissionModel.objects.all()
    lookup_field = 'user'

    def list(self, request, *args, **kwargs):
        ser = self.get_serializer(self.get_queryset(), many=True)
        return Response(ser.data[0])


class ManagePermissionAccessView(generics.RetrieveUpdateAPIView):
    """
    Custom permission added for all user
    """
    permission_classes = [custom_permission.EmployeeAuthenticated, custom_permission.IsSuperUser]
    serializer_class = hrm_admin_serializer.ManagePermissionAccessSerializer
    queryset = hrm_admin_model.ModulePermissionModel.objects.all()
    lookup_field = 'employee__user_id'


class EmployeeTrainingView(generics.ListCreateAPIView):
    """employee training information add List"""
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeTrainingSerializer

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            return hrm_admin_model.TrainingModel.objects.filter(Q(department__department__icontains=search) |
                                                                Q(training_name__icontains=search))
        except:
            return hrm_admin_model.TrainingModel.objects.all()


class EmployeeTrainingUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """employee training information add List"""
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeTrainingSerializer
    queryset = hrm_admin_model.TrainingModel.objects.all()
    lookup_field = 'id'


# Employee department and designation
class DepartmentsView(generics.ListCreateAPIView):
    """
    add new departments view
    """
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.DepartmentsSerializer

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            queryset = user_model.UserDepartmentModel.objects.filter(Q(departmentHead__full_name__icontains=search) |
                                                                     Q(department__icontains=search))
        except:
            queryset = user_model.UserDepartmentModel.objects.all()
        return queryset


class DepartmentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update delete existing departments view
    """
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.DepartmentsSerializer
    queryset = user_model.UserDepartmentModel.objects.all()
    lookup_field = 'id'


class DesignationsView(generics.ListCreateAPIView):
    """
    add new departments view
    """
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.DesignationsSerializer
    queryset = user_model.UserDesignationModel.objects.all()

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            queryset = user_model.UserDesignationModel.objects.filter(Q(designation__icontains=search) |
                                                                      Q(department__department__icontains=search))
        except:
            queryset = user_model.UserDesignationModel.objects.all()
        return queryset


class DesignationUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update delete existing departments view
    """
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.DesignationsSerializer
    queryset = user_model.UserDesignationModel.objects.all()
    lookup_field = 'id'

#employee resignation list view
class EmployeeResignationView(generics.ListAPIView):
    """
    Employee resignation
    """
    permission_classes = [custom_permission.IsHrOrReadOnly]
    serializer_class = hrm_admin_serializer.EmployeeResignationSerializer
    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            queryset = hrm_user_models.ResignationModel.objects.all()
            print(queryset.filter(Q(employee__user__full_name__icontains=search)))
            return queryset.filter(Q(employee__user__full_name__icontains=search) |
                                   Q(employee__emp_department__department__icontains=search))
        except:
            return hrm_user_models.ResignationModel.objects.all()

class EmployeeResignationUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Employee resignation update and delete
    """
    permission_classes = [custom_permission.IsHrOrReadOnly]
    serializer_class = hrm_admin_serializer.EmployeeResignationSerializer
    queryset = hrm_user_models.ResignationModel.objects.all()
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.resignatioAcceptDate=datetime.date(datetime.now())
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)