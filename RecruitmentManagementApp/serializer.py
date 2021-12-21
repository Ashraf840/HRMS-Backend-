from rest_framework import serializers
# from rest_framework.utils.serializer_helpers import ReturnDict

from UserApp import serializer
from UserApp.models import User
from . import models


# Viewing all user information from admin panel
class AllUserDetailsSerializer(serializers.ModelSerializer):
    academicInfo = serializer.UserAcademicSerializer(source='academic_info_user', many=True)
    certificationInfo = serializer.UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = serializer.UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = serializer.UserJobPreferenceSerializer(source='job_preference_user', many=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


# Job post Model Serializer -> Only for HR
class FilterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobApplyFilterQuestionModel
        fields = '__all__'


class JobPostSerializer(serializers.ModelSerializer):
    # filterQus = FilterQuestionSerializer()

    class Meta:
        model = models.JobPostModel
        exclude = ['user']
        extra_kwargs = {
            'user': {'read_only': True},

        }
        depth = 1

    # def create(self, validated_data):
    #     print(validated_data)
    #     filterQus = validated_data.pop('filterQus')
    #
    #     return filterQus


class OnlineTestSerializer(serializers.ModelSerializer):
    jobInfo = JobPostSerializer()
    filterQus = serializers.PrimaryKeyRelatedField(queryset=models.JobApplyFilterQuestionModel.objects.all(),
                                                   write_only=True, many=True)
    progressStatus = serializers.PrimaryKeyRelatedField(queryset=models.JobStatusModel.objects.all(), write_only=True,
                                                        many=True)

    class Meta:
        model = models.OnlineTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }

    def create(self, validated_data):
        # print(validated_data)
        jobData = validated_data.pop('jobInfo')
        # onlineTestData = validated_data.pop('onlineTest')
        question = validated_data.pop('filterQus')
        progress = validated_data.pop('progressStatus')
        # print(question)
        jobInfo = models.JobPostModel.objects.create(user_id=self.context['request'].user.id,
                                                     **jobData)
        jobInfo.filterQuestions.add(*question)
        jobInfo.jobProgressStatus.add(*progress)
        # print(jobInfo.filterQuestions.set(filterQus))
        onlineTest = models.OnlineTestModel.objects.create(jobInfo_id=jobInfo.id, **validated_data)
        return onlineTest


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobStatusModel
        fields = '__all__'


class PracticalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    # def create(self, validated_data):
    #     print(validated_data)
    #     jobData = validated_data.pop('jobInfo')
    #     validated_data.pop('cultural_test')
    #     validated_data.pop('analytical_test')
    #     # onlineTestData = validated_data.pop('onlineTest')
    #     # filterQus = jobData.pop('filterQuestions')
    #
    #     # jobInfo = models.JobPostModel.objects.create(user_id=self.context['request'].user.id, **jobData)
    #     # jobInfo.filterQuestions.set(filterQus)
    #     # onlineTest = models.OnlineTestModel.objects.create(jobInfo_id=jobInfo.id, **onlineTestData)
    #     practicalTest = models.PracticalTestModel.objects.create(jobInfo_id=jobData.id, **validated_data)
    #     return practicalTest


class FilterQuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilterQuestionsResponseModelHR
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
        }


"""
Job progress functionality section
Job application functionality ,
step by step status changes
"""


class AppliedForJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }


class MyJobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'

        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }
        depth = 1

    def to_representation(self, instance):
        data = super(MyJobListSerializer, self).to_representation(instance)
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

        data.get('jobPostId').pop('filterQuestions')
        print(data.get('jobPostId'))

        return data


class CandidateStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            # 'jobProgressStatus': {'read_only': True},
            'jobPostId': {'read_only': True}
        }


class OnlineTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OnlineTestResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'appliedJob': {'read_only': True},
        }


class PracticalTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'appliedJob': {'read_only': True},
        }
