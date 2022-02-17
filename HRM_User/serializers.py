from rest_framework import serializers
from HRM_User import models as hrm_user_model


class EmployeeTrainingResponseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_user_model.EmployeeTrainingResponseResultModel
        fields = '__all__'
        extra_kwargs = {
            'employee': {'read_only': True}
        }
