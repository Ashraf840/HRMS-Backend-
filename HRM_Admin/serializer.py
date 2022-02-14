from rest_framework import serializers
from HRM_Admin import models as hrm_admin
from UserApp import models as user_model


class EmployeeInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = '__all__'


class SalaryInfoSerializer(serializers.ModelSerializer):
    employee = EmployeeInformationSerializer()

    class Meta:
        model = hrm_admin.EmployeeSalaryModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }

    def create(self, validated_data):
        employeeInfo = validated_data.pop('employee')
        employee = hrm_admin.EmployeeInformationModel.objects.create(**employeeInfo)
        salary = hrm_admin.EmployeeSalaryModel.objects.create(employee=employee, **validated_data)
        return salary
