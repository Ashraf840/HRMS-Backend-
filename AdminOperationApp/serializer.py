from rest_framework import serializers

from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel





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
    # totalApplied = serializers.CharField(source='')
    total_count = serializers.SerializerMethodField('_checked')

    def _checked(self, filters):
        total = getattr(filters, 'total_applied')
        return total

    class Meta:
        model = JobPostModel
        fields = '__all__'







