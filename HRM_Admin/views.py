from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from HRM_Admin import models as hrm_admin_model, serializer as hrm_admin_serializer
from UserApp import models as user_model, permissions as custom_permission, utils
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


# Create your views here.
# class OnboardAnEmployeeView(generics.ListCreateAPIView):
#     permission_classes = [custom_permission.EmployeeAuthenticated]
#     serializer_class = hrm_admin_serializer.EmployeeInformationSerializer
#     queryset = hrm_admin_model.EmployeeInformationModel.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         checkDesignation = user_model.UserDesignationModel.objects.get(id=request.data['designation'])
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         userInfo = user_model.User.objects.get(id=request.data['user'])
#         if checkDesignation.designation != 'CEO':
#             self.perform_create(serializer)
#             if checkDesignation.designation == 'HR':
#                 userInfo.is_hr = True
#         else:
#             if userInfo.is_superuser:
#                 self.perform_create(serializer)
#             else:
#                 return Response({'message': 'You are not superuser'})
#         userInfo.is_candidate = False
#         userInfo.is_employee = True
#         userInfo.save()
#         return Response(serializer.data)


class AddEmployeeInfoView(generics.CreateAPIView):
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = hrm_admin_serializer.SalaryInfoSerializer
    queryset = hrm_admin_model.EmployeeSalaryModel

    def create(self, request, *args, **kwargs):
        checkDesignation = user_model.UserDesignationModel.objects.get(id=request.data.get('employee.designation'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        userInfo = user_model.User.objects.get(id=request.data['employee.user'])
        if checkDesignation.designation != 'CEO':
            self.perform_create(serializer)
            if checkDesignation.designation == 'HR':
                userInfo.is_hr = True
        else:
            if userInfo.is_superuser:
                self.perform_create(serializer)
            else:
                return Response({'message': 'You are not superuser'})

        userInfo.is_candidate = False
        userInfo.is_employee = True
        userInfo.email_validated = False
        userInfo.email = request.data['employee.official_email']
        userInfo.save()

        # Email activation email.
        token = RefreshToken.for_user(userInfo).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('tfhrm_api:employee-email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        email_body = f'Hi {userInfo.full_name},\n' \
                     f'Congratulation you profile has been updated. Please verify email and login into hrm site.' \
                     f'Verification link {absurl}'

        data = {'email_body': email_body, 'to_email': userInfo.email,
                'email_subject': 'Verification Email'}

        utils.Util.send_email(data)

        return Response(serializer.data)
