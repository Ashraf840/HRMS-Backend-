from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
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
    non_field_errors = {
        'detail': 'Please verify your mail.'
    }
    default_error_messages = {
        'detail': 'Username or Password does not matched.'
    }

    def validate(self, attrs):
        # print(attrs)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # print(data)
        if self.user.email_validated:
            obj = {
                'id': self.user.id,
                'email': self.user.email,
                'full_name': self.user.full_name,
                'phone_number': self.user.phone_number,
                'is_candidate': self.user.is_candidate,
                'is_hr': self.user.is_hr,
                'is_employee': self.user.is_employee,
                'email_validated': self.user.email_validated,

            }
            data.update({'user': obj})
            return data

        else:
            msg = "You email is not verified.please chek your email and verify to login"

        raise serializers.ValidationError(msg)


# User model Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], \
                                     style={'input_type': 'password'})

    # password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ('full_name', 'email', 'birthDate', 'gender', 'phone_number', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'birthDate': {'required': True},
            # 'nationality': {'required': True},
            'password': {'write_only': True},
            'phone_number': {'write_only': True},

        }

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #
    #     return attrs

    def create(self, validated_data):
        user = models.User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            birthDate=validated_data['birthDate'],
            # nationality=validated_data['nationality'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],

        )

        user.set_password(validated_data['password'])
        user.save()
        return user
        # return models.User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = models.User
        fields = ['token']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('full_name', 'birthDate', 'nationality', 'phone_number', 'gender', 'location', 'nid', 'profile_pic')
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'birthDate': {'required': True},
            'nationality': {'required': True},

        }

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.birthDate = validated_data.get('birthDate', instance.birthDate)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.location = validated_data.get('location', instance.location)
        instance.nid = validated_data.get('nid', instance.nid)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


# User Information serializer
class UserSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    # userAcademicInfo = UserAcademicInfoSerializer()

    class Meta:
        model = models.UserInfoModel
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

class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfoModel
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserAcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True}
        }
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
        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserWorkingExperienceModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserTrainingExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTrainingExperienceModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserJobPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPreferenceModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


# User Detailed View
"""
user Basic Info -> User
User More info -> UserInfoModel
Academic Information -> UserAcademicInfoModel
Certification Information -> UserCertificationsModel
Training Information -> UserTrainingModel
"""


class UserDetailsSerializer(serializers.ModelSerializer):
    userInfo = UserInformationSerializer(source='user_info_user')
    academicInfo = UserAcademicSerializer(source='academic_info_user', many=True)
    certificationInfo = UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = UserJobPreferenceSerializer(source='job_preference_user', many=True)
    workExperience = UserWorkExperienceSerializer(source='working_experience_user', many=True)

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
        extra_kwargs = {
            'user': {'read_only': True}
        }

    # def save(self, **kwargs):
    #     user = None
    #     request = self.context.get("request")
    #     if request and hasattr(request, "id"):
    #         user = request.id
    #         print(user)


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SkillsModel
        fields = "__all__"


class DocumentationSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentSubmissionModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class ReferenceInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferenceInformationModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only':True}
        }