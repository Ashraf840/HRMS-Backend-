from rest_framework import serializers
from HRM_controller import models
from UserApp import models as user_models
from HRM_Admin import models as hrm_models
from HRM_User import models as user_models_hrm



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


class SurveyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyUserResponseModel
        fields = '__all__'


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


# Announcement, Notice and Complain Section
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnouncementModel
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NoticeModel
        fields = '__all__'


class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplainModel
        fields = '__all__'

        extra_kwargs = {
            'is_resolved': {
                'read_only': True
            }
        }


class ComplainResolvedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplainModel
        fields = '__all__'

        extra_kwargs = {
            'complain_reason': {
                'read_only': True
            },
            'complain_details': {
                'read_only': True
            },
            'complain_at': {
                'read_only': True
            },
        }


# ============ Attendance Section ============
class CreateHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HolidayModel
        fields = '__all__'


class AttendanceShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceShiftTimeModel
        fields = '__all__'


class AttendanceRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendanceEmployeeRelModel
        fields = '__all__'


class EmployeeAttendanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeAttendanceLogModel
        fields = '__all__'

# ============ Promotion Section ============
class EmployeePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeePromotionModel
        fields = '__all__'

class TerminationTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TerminationTitleModel
        fields = '__all__'

#Employee termination serializer
class EmployeeTerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeTerminationModel
        fields = '__all__'
