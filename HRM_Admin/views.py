import datetime
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics
from HRM_Admin import models as hrm_admin_model, serializer as hrm_admin_serializer
from UserApp import models as user_model, permissions as custom_permission, utils
from AdminOperationApp import models as admin_operation_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# email formatting library file
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


# Create your views here.
class OnboardAnEmployeeView(generics.ListCreateAPIView):
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = hrm_admin_serializer.OnboardNewEmployeeSerializer
    queryset = hrm_admin_model.EmployeeSalaryModel.objects.all()

    def create(self, request, *args, **kwargs):
        checkDesignation = user_model.UserDesignationModel.objects.get(id=request.data['employee'].get('user'))
        userInfo = user_model.User.objects.get(id=request.data['employee'].get('user'))
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
        userInfo.email = request.data['employee'].get('email')
        userInfo.save()

        # Email activation email.
        token = RefreshToken.for_user(userInfo).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('tfhrm_api:employee-email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        email_body = f'Hi {userInfo.full_name},\n' \
                     f'Congratulation you profile has been updated. Please verify email and login into hrm site.' \
                     f'Verification link {absurl}'

        # html_message = render_to_string('html.html', context={})
        # plain_message = strip_tags(html_message)
        # email = EmailMultiAlternatives(
        #     'subject',
        #     plain_message,
        #     'pranto.techforing@gmail.com',
        #     ['zulkar.techforing@gmail.com']
        # )
        # email.attach_alternative(html_message,'text/html')
        # email.send()
        # email_body = plain_message

        data = {'email_body': email_body, 'to_email': userInfo.email,
                'email_subject': 'Verification Email'}

        utils.Util.send_email(data)
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
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

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
        search = self.request.query_params.get('search')
        queryset = hrm_admin_model.EmployeeInformationModel.objects.all()
        return queryset.filter(Q(user__full_name__icontains=search) |
                               Q(emp_department__department__icontains=search) |
                               Q(designation__designation__icontains=search) |
                               Q(user__email__icontains=search))

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


class ManagePermissionAccessView(generics.RetrieveUpdateAPIView):
    """
    Custom permission added for all user
    """
    permission_classes = [custom_permission.EmployeeAuthenticated, custom_permission.IsSuperUser]
    serializer_class = hrm_admin_serializer.ManagePermissionAccessSerializer
    queryset = hrm_admin_model.ModulePermissionModel.objects.all()
    lookup_field = 'employee__user_id'


class EmployeeTrainingView(generics.ListCreateAPIView):
    """employee training information add"""
    permission_classes = [custom_permission.EmployeeAdminAuthenticated]
    serializer_class = hrm_admin_serializer.EmployeeTrainingSerializer
    queryset = hrm_admin_model.TrainingModel.objects.all()

