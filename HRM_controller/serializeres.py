from rest_framework import serializers
from HRM_controller import models
from UserApp import models as user_models
from HRM_Admin import models as hrm_models
from HRM_User import models as user_models_hrm



# Survey Section
class SurveyQuestionSerializer(serializers.ModelSerializer):
    # answers = serializers.SlugRelatedField(queryset=models.SurveyAnswerSheetModel.objects.all(), many=True,
    #                                        slug_field='answers')

    # answers = serializers.StringRelatedField(many=True)
    # created_date = serializers.DateField(format='%m/%d/%Y')
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
    question=SurveyQuestionSerializer()
    class Meta:
        model = models.SurveyUserResponseModel
        # fields = ['id','question','answer','question_id','is_answered','ans_time']
        fields='__all__'


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
    # department=user_serializer.UserDepartmentSerializer(read_only=True,many=True)
    class Meta:
        model = models.AnnouncementModel
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    employee=serializers.SlugRelatedField(read_only=True,many=True,slug_field='full_name')
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
    # holiday_date = serializers.DateField(format='%B-%d-%Y')
    class Meta:
        model = models.HolidayModel
        fields = '__all__'
        extra_kwargs = {
            'is_active': {
                'read_only': True
            },
            'month':{
                'read_only':True
            }
        }


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
    # promotion_to=serializers.StringRelatedField()
    # employee=serializers
    employee_name=serializers.SerializerMethodField()
    promotion_to_name=serializers.SerializerMethodField()
    class Meta:
        model = models.EmployeePromotionModel
        fields = '__all__'
        # depth=1
    def get_employee_name(self,object):
        return object.employee.user.full_name
    
    def get_promotion_to_name(self,object):
        return object.promotion_to.designation

class EmployeePromotionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeePromotionModel
        fields = '__all__'
        depth=2

class TerminationTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TerminationTitleModel
        fields = '__all__'


'''
----------------------Birthday section----------------------------
'''

class EmployeeBirthdayListSerializer(serializers.ModelSerializer):
    emp_department=serializers.StringRelatedField()
    designation=serializers.StringRelatedField()
    birthday=serializers.SerializerMethodField()
    employee_name=serializers.SerializerMethodField()
    class Meta:
        model=hrm_models.EmployeeInformationModel
        fields='__all__'
        fields=['emp_department','designation','birthday','employee_name','shift','joining_date']
        # depth=1
    def get_birthday(self,object):
        return object.user.birthDate
    def get_employee_name(self,object):
        return object.user.full_name


'''
----------------------Termination section----------------------------
'''
#Employee termination serializer
class EmployeeTerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployeeTerminationModel
        fields = '__all__'
