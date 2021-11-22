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


class AppliedForJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'


class UpdateAppliedJobSerializer(serializers.ModelSerializer):
    jobInfo = AppliedForJobSerializer(source='job_post_id', many=True)

    class Meta:
        model = models.JobPostModel
        fields = '__all__'
