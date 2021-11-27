from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, UserInfoModel
from . import models

# class UserInfoModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInfoModel
#         fields= '__all__'


"""
-> request user verification code 

    def get(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            print(user)
"""


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # info = serializers.CharField(source='permission_user')
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        obj = {
            'email': self.user.email,
            'id': self.user.id,

        }
        data.update({'obj': obj})

        return data


# User model Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], \
                                     style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('full_name', 'email', 'birthDate', 'nationality', 'phone_number','gender','password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'birthDate': {'required': True},
            'nationality': {'required': True},

        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            birthDate=validated_data['birthDate'],
            nationality=validated_data['nationality'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],

        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


# User Information serializer
class UserSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    # userAcademicInfo = UserAcademicInfoSerializer()

    class Meta:
        model = UserInfoModel
        fields = '__all__'


#         depth = 1
# extra_kwargs = {
#     'password': {'write_only': True}
# }

# def create(self, validated_data):
#     password = validated_data.pop('password', None)
#     instance = self.Meta.model(**validated_data)
#     if password is not None:
#         instance.set_password(password)
#     instance.save()
#     return instance


# User Details serializer
class UserAcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'
        # depth = 1

    # def save(self, **kwargs):
    #     request = self.context.get("request")
    #     # print(request)
    #     if request and hasattr(request, "user"):
    #         user = request.user
    #         # print(user)


class UserCertificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserCertificationsModel
        fields = '__all__'


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWorkingExperienceModel
        fields = '__all__'


class UserTrainingExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTrainingExperienceModel
        fields = '__all__'


class UserJobPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPreferenceModel
        fields = '__all__'


# User Detailed View
"""
user Basic Info -> User
User More info -> UserInfoModel
Academic Information -> UserAcademicInfoModel
Certification Information -> UserCertificationsModel
Training Information -> UserTrainingModel
"""


class UserDetailsSerializer(serializers.ModelSerializer):
    academicInfo = UserAcademicSerializer(source='academic_info_user', many=True)
    certificationInfo = UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = UserJobPreferenceSerializer(source='job_preference_user', many=True)

    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


# Academic information update from frontend serializer
class UpdateAcademicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'

    # def save(self, **kwargs):
    #     user = None
    #     request = self.context.get("request")
    #     if request and hasattr(request, "id"):
    #         user = request.id
    #         print(user)
