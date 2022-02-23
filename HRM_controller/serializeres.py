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


class EmployeeEvaluationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeCriteriaModel
        fields = '__all__'


class EmployeeEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeEvaluationModel
        fields = '__all__'
        extra_kwargs = {
            'sender_user': {
                'read_only': True
            },
            'receiver_user': {
                'read_only': True
            }
        }


# Announcement/Notice Section
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnouncementModel
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NoticeModel
        fields = '__all__'


# Attendance Section
class CreateHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HolidayModel
        fields = '__all__'


class AttendanceShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceEmployeeShiftModel
        fields = '__all__'


class AttendanceRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceEmployeeRelModel
        fields = '__all__'
