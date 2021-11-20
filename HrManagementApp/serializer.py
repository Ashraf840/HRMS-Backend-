from rest_framework import serializers
from UserApp import serializer
from UserApp.models import User


# Viewing all user information from admin panel
class AllUserDetailsSerializer(serializers.ModelSerializer):
    academicInfo = serializer.UserAcademicSerializer(source='academic_info_user', many=True)
    certificationInfo = serializer.UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = serializer.UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = serializer.UserJobPreferenceSerializer(source='job_preference_user', many=True)

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', ]
        # depth = 2