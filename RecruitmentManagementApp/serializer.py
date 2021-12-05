from rest_framework import serializers
from UserApp import serializer
from UserApp.models import User
from . import models
from .models import FilterQuestionsResponseModelHR


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
    class Meta:
        model = models.OnlineTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }


class PracticalTestSerializer(serializers.ModelSerializer):
    jobPost = JobPostSerializer()
    onlineTest = OnlineTestSerializer()


    class Meta:
        model = models.PracticalTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        jobData = validated_data.pop('jobPost')
        onlineTestData = validated_data.pop('onlineTest')
        jobPost = models.JobPostModel.objects.create(**jobData)
        onlineTest = models.OnlineTestModel.objects.create(jobInfo_id=jobPost, **onlineTestData)
        practicalTest = models.PracticalTestModel.objects.create(jobInfo_id=jobPost, **validated_data)
        return practicalTest


class AppliedForJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True}
        }


# class UpdateAppliedJobSerializer(serializers.ModelSerializer):
#     # jobInfo = AppliedForJobSerializer(source='job_post_id', many=True)
#
#     class Meta:
#         model = models.UserJobAppliedModel
#         fields = '__all__'

class FilterQuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilterQuestionsResponseModelHR
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},

        }
