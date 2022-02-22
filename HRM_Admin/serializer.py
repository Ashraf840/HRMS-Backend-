from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from HRM_Admin import models as hrm_admin
from UserApp import models as user_model, serializer as user_serializer


# class EmployeeUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = user_model.User
#         fields = ['full_name']


class EmployeeInformationListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=user_model.User.objects.all(), slug_field='full_name')
    designation = serializers.SlugRelatedField(queryset=user_model.UserDesignationModel.objects.all(),
                                               slug_field='designation')
    emp_department = serializers.SlugRelatedField(queryset=user_model.UserDepartmentModel.objects.all(),
                                                  slug_field='department')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['id', 'user', 'designation', 'emp_department', 'phone_number', 'email', 'joining_date']


class EmployeeInformationCreateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(validators=[UniqueValidator(queryset=user_model.User.objects.all(),
    #                                                            message="Name already exists")])

    user = user_serializer.RegisterSerializer()

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['user', 'designation', 'emp_department', 'joining_date']


class SalaryInfoSerializer(serializers.ModelSerializer):
    # user = user_serializer.RegisterSerializer()
    employee = EmployeeInformationCreateSerializer()

    class Meta:
        model = hrm_admin.EmployeeSalaryModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True},
            # 'salary': {'read_only': True}
        }

    def create(self, validated_data):
        employeeInfo = validated_data.pop('employee')
        user = employeeInfo.pop('user')
        # employeeInfo.pop('email')
        userData = user_model.User.objects.create(**user)
        employee = hrm_admin.EmployeeInformationModel.objects.create(user=userData, **employeeInfo)
        salary = hrm_admin.EmployeeSalaryModel.objects.create(employee=employee, **validated_data)

        return salary


# Employee information serializers
class EmployeeEmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.EmployeeEmergencyContactModel
        fields = '__all__'


class EmployeeBankInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.EmployeeBankInfoModel
        fields = '__all__'


class EmployeeInfoSerializer(serializers.ModelSerializer):
    employeeEmergencyContactInfo = EmployeeEmergencyContactSerializer(source='employee_emergency_contact_info',
                                                                      many=True)
    employeeSalaryInfo = EmployeeBankInformationSerializer(source='employee_bank_info')

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = '__all__'


class EmployeeInformationSerializer(serializers.ModelSerializer):
    academicInfo = user_serializer.UserAcademicDetailsSerializer(source='academic_info_user', many=True)
    certificationInfo = user_serializer.UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = user_serializer.UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = user_serializer.UserJobPreferenceSerializer(source='job_preference_user', many=True)
    workExperience = user_serializer.UserWorkExperienceSerializer(source='working_experience_user', many=True)
    userSkills = user_serializer.UserSkillsSerializer(source='skills_user')
    employeeInfo = EmployeeInfoSerializer(source='employee_user_info')

    class Meta:
        model = user_model.User

        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        data = super(EmployeeInformationSerializer, self).to_representation(instance)
        data.pop('groups')
        data.pop('last_login')
        data.pop('user_permissions')
        data.pop('email_validated')
        data.pop('date_joined')
        return data


class ManagePermissionAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.ModulePermissionModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }


class EmployeeTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.TrainingModel
        fields = '__all__'
