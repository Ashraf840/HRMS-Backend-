from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from HRM_Admin import models as hrm_admin
from UserApp import models as user_model


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model.User
        fields = ['full_name']


class EmployeeInformationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=user_model.User.objects.all(), slug_field='full_name')
    designation = serializers.SlugRelatedField(queryset=user_model.UserDesignationModel.objects.all(),
                                               slug_field='designation')
    emp_department = serializers.SlugRelatedField(queryset=user_model.UserDepartmentModel.objects.all(),
                                                  slug_field='department')
    email = serializers.EmailField(validators=[UniqueValidator(queryset=user_model.User.objects.all(),
                                                               message="Name already exists")])

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['user', 'designation', 'emp_department', 'email', 'joining_date']


class EmployeeInformationCreateSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(queryset=user_model.User.objects.all(), slug_field='full_name')
    # designation = serializers.SlugRelatedField(queryset=user_model.UserDesignationModel.objects.all(),
    #                                            slug_field='designation')
    # emp_department = serializers.SlugRelatedField(queryset=user_model.UserDepartmentModel.objects.all(),
    #                                               slug_field='department')
    email = serializers.EmailField(validators=[UniqueValidator(queryset=user_model.User.objects.all(),
                                                               message="Name already exists")])

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['user', 'designation', 'emp_department', 'email', 'joining_date']


class SalaryInfoSerializer(serializers.ModelSerializer):
    employee = EmployeeInformationCreateSerializer()

    class Meta:
        model = hrm_admin.EmployeeSalaryModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }

    def create(self, validated_data):
        employeeInfo = validated_data.pop('employee')
        employeeInfo.pop('email')
        employee = hrm_admin.EmployeeInformationModel.objects.create(**employeeInfo)

        salary = hrm_admin.EmployeeSalaryModel.objects.create(employee=employee, **validated_data)
        return salary
