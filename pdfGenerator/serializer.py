from rest_framework import serializers
from RecruitmentManagementApp.models import OfficialDocumentsModel


class ViewAppointMentLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialDocumentsModel
        fields = '__all__'

