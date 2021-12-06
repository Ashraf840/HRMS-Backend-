from rest_framework import serializers
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

        # depth = 2


# Job post Model Serializer -> Only for HR


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPostModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class OnlineTestSerializer(serializers.ModelSerializer):
    jobInfo = JobPostSerializer()

    class Meta:
        model = models.OnlineTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        jobData = validated_data.pop('jobInfo')
        # onlineTestData = validated_data.pop('onlineTest')
        filterQus = jobData.pop('filterQuestions')

        jobInfo = models.JobPostModel.objects.create(user_id=self.context['request'].user.id, **jobData)
        jobInfo.filterQuestions.set(filterQus)
        onlineTest = models.OnlineTestModel.objects.create(jobInfo_id=jobInfo.id, **validated_data)
        return onlineTest


# class FilterQusSerializer(serializers.ModelSerializer):
#     jobPost = JobPostSerializer()


class PracticalTestSerializer(serializers.ModelSerializer):
    # jobInfo = JobPostSerializer()

    # jobInfo = OnlineTestSerializer()

    class Meta:
        model = models.PracticalTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
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


class OnlineTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OnlineTestResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }


class PracticalTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }
