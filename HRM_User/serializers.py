from rest_framework import serializers
from HRM_User import models as hrm_user_model


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
    class Meta:
        model = hrm_user_model.LeaveRequestModel
        fields = '__all__'
        extra_kwargs = {
            'no_of_days': {'read_only': True},
            'status': {'read_only': True},
            'approved_by': {'read_only': True},
            'employee': {'read_only': True},
        }
