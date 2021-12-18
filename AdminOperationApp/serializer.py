from rest_framework import serializers

from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel
from RecruitmentManagementApp.serializer import OnlineTestResponseSerializer


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


# selected user for interview. will show online,practical test result will show
class AdminInterviewerListSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        serializer = super(AdminInterviewerListSerializer, self).to_representation(instance)
        serializer.get('userId').pop('password')
        # testRes =
        return serializer


class AdminOnlineTestLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }
