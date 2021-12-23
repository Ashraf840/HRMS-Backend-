from rest_framework import serializers

import UserApp.models
from . import models
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel, OnlineTestResponseModel, \
    PracticalTestModel
from RecruitmentManagementApp.serializer import OnlineTestResponseSerializer, PracticalTestResponseSerializer, \
    PracticalTestSerializer


class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp.models.UserDepartmentModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Return user basic information
    """

    class Meta:
        model = UserApp.models.User
        fields = ['id', 'email', 'full_name', 'profile_pic', 'phone_number', 'nid', 'nationality']


class JobSerializer(serializers.ModelSerializer):
    # filterQus = FilterQuestionSerializer()

    class Meta:
        model = JobPostModel
        fields = ['id', 'jobTitle']


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


class AdminDashboardSerializer(serializers.ModelSerializer):
    """
    Admin Dashboard serializer
    return Job applied information
    and manually
    """
    jobPostId = JobSerializer()
    userId = UserSerializer()

    # print(jobPostId)
    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        # depth = 1

    # def to_representation(self, instance):
    #     data = super(AdminDashboardSerializer, self).to_representation(instance)
    #     jobInfo = data.get('jobPostId')
    #     # print(jobInfo)
    #     # jobInfo.pop('id')
    #     # jobInfo.pop('filterQuestions')
    #     # jobInfo.pop('jobProgressStatus')
    #     # jobInfo.pop('is_active')
    #     # jobInfo.pop('jobDescription')
    #     # jobInfo.pop('jobType')
    #     # jobInfo.pop('lastUpdated')
    #     # jobInfo.pop('postDate')
    #     # jobInfo.pop('department')
    #     # jobInfo.pop('vacancies')
    #
    #     return data


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
    onlineTest = OnlineTestResponseSerializer(source='job_applied_online_response', many=True)
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
