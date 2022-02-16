from rest_framework import serializers
from HRM_controller import models
from UserApp import models as user_models
from HRM_Admin import models as hrm_models


# Survey Section
class SurveyQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SlugRelatedField(queryset=models.SurveyAnswerSheetModel.objects.all(), many=True,
                                           slug_field='answers')

    # answers = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.SurveyQuestionModel
        fields = '__all__'


class SurveyUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyUserResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'is_answered': {
                'read_only': True
            },
            'months': {
                'read_only': True
            }
        }


# Employee Evaluation Section

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = ['id', 'email', 'full_name', 'profile_pic', 'phone_number']


class EmployeeDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.UserDepartmentModel
        fields = ['id', 'department']


class AllColleaguesSerializer(serializers.ModelSerializer):
    user = AllUserSerializer()
    emp_department = serializers.CharField(source='emp_department.department')

    class Meta:
        model = hrm_models.EmployeeInformationModel
        fields = ['user', 'emp_department']
        # depth = 2

    # def to_representation(self, instance):
    #     data = super(AllColleaguesSerializer, self).to_representation(instance)
    #     user = data.get('user')
    #     # emp_department = data.get('emp_department')
    #
    #     user.pop('password')
    #     user.pop('last_login')
    #     user.pop('nid')
    #     user.pop('nationality')
    #     user.pop('location')
    #     user.pop('birthDate')
    #     user.pop('date_joined')
    #     user.pop('gender')
    #     user.pop('is_staff')
    #     user.pop('is_active')
    #     user.pop('email_validated')
    #     user.pop('is_superuser')
    #     user.pop('is_employee')
    #     user.pop('is_hr')
    #     user.pop('is_candidate')
    #     user.pop('groups')
    #     user.pop('user_permissions')
    #
    #     return data
