from asyncore import read
from multiprocessing import managers
from rest_framework import serializers
from HRM_User import models as hrm_user_model
from UserApp import permissions as custom_permission
from serializer_permissions import serializers as permission_ser
from HRM_Admin import serializer as hrm_admin_ser


class EmployeeTrainingResponseResultSerializer(serializers.ModelSerializer):
    """
    Employee training information response will be serialized here
    """

    class Meta:
        model = hrm_user_model.EmployeeTrainingResponseResultModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }


#  ================= Employee Leave Section =================
class EmployeeLeaveRequestSerializer(serializers.ModelSerializer):
    status = permission_ser.CharField(permission_classes=(custom_permission.IsHrOrReadOnly,), hide=True)

    class Meta:
        model = hrm_user_model.LeaveRequestModel
        fields = '__all__'
        extra_kwargs = {
            'no_of_days': {'read_only': True},
            # 'status': {'read_only': True},
            'approved_by': {'read_only': True},
            'employee': {'read_only': True},
        }

#  ================= Employee Resignation Section =================
class EmployeeResignationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_user_model.ResignationModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True},
            'resignationstaus': {'read_only': True},
            'resignatioAcceptDate': {'read_only': True},
        }

#exit interview section
class ExitInterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_user_model.ExitInterviewQuestionModel
        fields = '__all__'
        
class ExitInterviewAnswerSerializer(serializers.ModelSerializer):
    # resignation=EmployeeResignationRequestSerializer(source='exit_interview_answer_employee')
    question=ExitInterviewQuestionSerializer(read_only=True)
    employee=hrm_admin_ser.EmployeeInformationListSerializer(read_only=True)
    class Meta:
        model = hrm_user_model.ExitInterviewAnswerModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True},
            # 'question': {'read_only': True},
        }
    
        