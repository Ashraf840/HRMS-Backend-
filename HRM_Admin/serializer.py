from rest_framework import serializers
from HRM_Admin import models as hrm_admin


class EmployeeInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = hrm_admin.models
        fields = '__all__'
