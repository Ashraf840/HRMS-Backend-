from rest_framework import serializers
from . import models
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel, OnlineTestResponseModel, \
    PracticalTestModel
from RecruitmentManagementApp.serializer import OnlineTestResponseSerializer, PracticalTestResponseSerializer,PracticalTestSerializer


class AdminOnlineTestLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }


class SendPracticalTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PracticalTestUserModel
        fields = '__all__'
        extra_kwargs = {
            # 'user': {'read_only': True},
            # 'practicalTestInfo': {'read_only': True}
        }


class AdminJobListSerializer(serializers.ModelSerializer):
    """
    All posted job will be visible here and total no of applicant will be shown here
    """

    total_count = serializers.SerializerMethodField('_checked')

    def _checked(self, filters):
        total = getattr(filters, 'total_applied')
        return total

    class Meta:
        model = JobPostModel
        fields = '__all__'


class AppliedUserDetailsSerializer(serializers.ModelSerializer):
    """
        Applicant list will be visible here in admin dashboard.
    """

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }
        depth = 1


class AdminAppliedCandidateOnlineResSerializer(serializers.ModelSerializer):
    """
    Online test response list and user info for admin panel online test dashboard
    """

    class Meta:
        model = OnlineTestResponseModel
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        data = super(AdminAppliedCandidateOnlineResSerializer, self).to_representation(instance)
        info = data.get('user')
        info.pop('password')
        info.pop('is_staff')
        info.pop('is_active')
        info.pop('email_validated')
        info.pop('is_superuser')
        info.pop('is_employee')
        info.pop('is_hr')
        info.pop('is_candidate')
        info.pop('groups')
        info.pop('user_permissions')
        info.pop('date_joined')
        data.get('appliedJob').pop('userId')

        return data


class AdminInterviewerListSerializer(serializers.ModelSerializer):
    """
    selected user for interview. will show online,practical test result will show
    """
    onlineTest = OnlineTestResponseSerializer(source='job_applied_online_response')
    practicalTest = PracticalTestResponseSerializer(source='job_applied_practical_response')

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super(AdminInterviewerListSerializer, self).to_representation(instance)
        # serializer.get('userId').pop('password')
        user = data.get('userId')
        user.pop('password')
        user.pop('is_staff')
        user.pop('is_active')
        user.pop('email_validated')
        user.pop('is_superuser')
        user.pop('is_employee')
        user.pop('is_hr')
        user.pop('is_candidate')
        user.pop('groups')
        user.pop('user_permissions')
        user.pop('date_joined')

        data.get('jobPostId').pop('filterQuestions')
        return data
