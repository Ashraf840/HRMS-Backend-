import datetime

from _testcapi import raise_exception
from django.shortcuts import render
from HRM_User import models, serializers
from HRM_Admin import models as hrm_admin_model, serializer as hrm_admin_serializer
from UserApp import permissions as custom_permission
from rest_framework import generics, response


# Create your views here.

class EmployeeTrainingResponseResultView(generics.ListCreateAPIView):
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = serializers.EmployeeTrainingResponseResultSerializer

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    def get_queryset(self):
        employeePermission = self.request.user.employee_user_info.module_permission_employee
        if employeePermission.is_superuser or employeePermission.is_hrm:
            queryset = models.EmployeeTrainingResponseResultModel.objects.all()
        else:
            queryset = models.EmployeeTrainingResponseResultModel.objects.filter(employee=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        ser = self.get_serializer(self.get_queryset(), many=True)
        employee = self.request.user.employee_test_result_user.all()
        training = models.EmployeeTrainingResponseResultModel.objects.all().count()
        if employee.count() == training:
            return response.Response({'message': 'Test Completed', 'response': ser.data})

        else:
            return response.Response(ser.data)

    def create(self, request, *args, **kwargs):
        check_response = models.EmployeeTrainingResponseResultModel.objects.filter(employee=self.request.user,
                                                                                   test=request.data['test'])
        if len(check_response) >= 1:
            return response.Response({'message': 'Already attempted this test'})
        else:
            ser = self.get_serializer(data=request.data)
            ser.is_valid(raise_exception=True)
            self.perform_create(ser)
        return response.Response(ser.data)


#  ================= Employee Leave Section =================
class EmployeeLeaveRequestView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    permission_classes = [custom_permission.EmployeeAuthenticated]
    serializer_class = serializers.EmployeeLeaveRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.is_hr or self.request.user.is_superuser:
            queryset = models.LeaveRequestModel.objects.all()
        else:
            queryset = models.LeaveRequestModel.objects.filter(employee__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        dateFrom = serializer.validated_data['leave_from']
        dateTo = serializer.validated_data['leave_to']
        countDay = dateTo - dateFrom
        employee = hrm_admin_model.EmployeeInformationModel.objects.get(user=self.request.user)
        serializer.save(employee=employee, no_of_days=countDay)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     if self.request.user.is_hr or self.request.user.is_superuser:
    #         employee = hrm_admin_model.EmployeeInformationModel.objects.get(user=self.request.user)
    #         serializer.update(approved_by=employee)
    #     return response.Response(serializer.data)

