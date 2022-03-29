from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from RecruitmentManagementApp import serializer as recruitment_serializer
from HRM_Admin import models as hrm_admin
from UserApp import models as user_model, serializer as user_serializer


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model.User
        fields = ['id', 'full_name']


class EmployeeUserUpdateDeleteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True)

    class Meta:
        model = user_model.User
        fields = ['id', 'email', 'full_name', 'phone_number', 'nid', 'nationality', 'location', 'birthDate', 'gender']


class EmployeeInformationListSerializer(serializers.ModelSerializer):
    """
    new employee add without career site.
    """
    user = EmployeeUserSerializer()
    designation = serializers.SlugRelatedField(queryset=user_model.UserDesignationModel.objects.all(),
                                               slug_field='designation')
    emp_department = serializers.SlugRelatedField(queryset=user_model.UserDepartmentModel.objects.all(),
                                                  slug_field='department')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.EmailField(source='user.phone_number')

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['id', 'user', 'designation', 'emp_department', 'phone_number', 'email', 'joining_date']


class EmployeeSerializer(serializers.ModelSerializer):
    """
        Employee information update during onboard session
    """
    email = serializers.EmailField(source='user.email',
                                   validators=[UniqueValidator(queryset=user_model.User.objects.all(),
                                                               message="Email already exists")])

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['email', 'user', 'designation', 'emp_department', 'joining_date']


class OnboardNewEmployeeSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = hrm_admin.EmployeeSalaryModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True},
            # 'salary': {'read_only': True}
        }

    def create(self, validated_data):
        employeeInfo = validated_data.pop('employee')
        # user = employeeInfo.pop('user')
        # employeeInfo.pop('email')
        # userData = user_model.User.objects.create(**user)
        employee = hrm_admin.EmployeeInformationModel.objects.create(**employeeInfo)
        salary = hrm_admin.EmployeeSalaryModel.objects.create(employee=employee, **validated_data)

        return salary


class EmployeeInformationCreateSerializer(serializers.ModelSerializer):
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


class EmployeeSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.EmployeeSalaryModel
        fields = ['salary',]


# Employee update section
class EmployeeUpdateDeleteSerializer(serializers.ModelSerializer):
    """
    Employee information update serializer
    """
    user = EmployeeUserUpdateDeleteSerializer()
    salary = EmployeeSalarySerializer(source='employee_salary_employee')
    emp_department = serializers.SlugRelatedField(queryset=user_model.UserDepartmentModel.objects.all(), slug_field='department')
    designation = serializers.SlugRelatedField(queryset=user_model.UserDesignationModel.objects.all(), slug_field='designation')

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = ['user', 'emp_department', 'designation', 'shift', 'joining_date', 'employee_is_permanent', 'salary']

    def update(self, instance, validated_data):
        # print(validated_data.pop('employee_salary_employee'))
        if 'user' in validated_data:
            nested_serializer = self.fields['user']
            nested_serializer_salary = self.fields['salary']
            nested_instance = instance.user
            nested_instance_salary = instance.employee_salary_employee
            nested_data = validated_data.pop('user')
            nested_salary = validated_data.pop('employee_salary_employee')

            email_valid = nested_data.get('email')
            if instance.user.email == email_valid:
                nested_data.pop('email')

            nested_serializer.update(nested_instance, nested_data)
            nested_serializer_salary.update(nested_instance_salary, nested_salary)
        return super(EmployeeUpdateDeleteSerializer, self).update(instance, validated_data)


# Employee extra information serializers
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
    employeeBankInfo = EmployeeBankInformationSerializer(source='employee_bank_info')
    employeeSalaryInfo = EmployeeSalarySerializer(source='employee_salary_employee')
    designation = serializers.StringRelatedField()
    emp_department = serializers.StringRelatedField()

    class Meta:
        model = hrm_admin.EmployeeInformationModel
        fields = '__all__'


class EmployeeInformationSerializer(serializers.ModelSerializer):
    """
    Employee details Information's
    """
    academicInfo = user_serializer.UserAcademicDetailsSerializer(source='academic_info_user', many=True)
    careerObjective = user_serializer.CareerObjectiveSerializer(source='career_objective_user')
    certificationInfo = user_serializer.UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = user_serializer.UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = user_serializer.UserJobPreferenceSerializer(source='job_preference_user', many=True)
    workExperience = user_serializer.UserWorkExperienceSerializer(source='working_experience_user', many=True)
    userSkills = user_serializer.UserSkillsSerializer(source='skills_user')
    references = recruitment_serializer.ReferenceInformationSerializer(source='reference_information_user', many=True)
    documents = recruitment_serializer.DocumentationSubmissionSerializer(source='document_submission_user', many=True)
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


# Employee permission
class ManagePermissionAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.ModulePermissionModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }


class EmployeeTrainingSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=user_model.UserDepartmentModel.objects.all(),
                                              slug_field='department')

    class Meta:
        model = hrm_admin.TrainingModel
        fields = '__all__'
