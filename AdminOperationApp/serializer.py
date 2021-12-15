from rest_framework import serializers
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel


class AppliedUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }
        depth = 1


class AdminJobListSerializer(serializers.ModelSerializer):

    totalApplied = serializers.CharField(source=UserJobAppliedModel.objects.filter())
    class Meta:
        model = JobPostModel
        fields = '__all__'

