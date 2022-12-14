from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from . import models
from django.contrib.sites.shortcuts import get_current_site

# class UserInfoModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeInfoModel
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
        if self.user.is_candidate:
            if self.user.is_active:
                if self.user.email_validated:
                    request = self.context.get('request')
                    if 'default.jpg' in request.build_absolute_uri(str(self.user.profile_pic.url)):
                        p_pic = 'default.jpg'
                    else:
                        p_pic = request.build_absolute_uri(str(self.user.profile_pic.url))
                    try:
                        obj = {
                            'id': self.user.id,
                            'email': self.user.email,
                            'full_name': self.user.full_name,
                            'phone_number': self.user.phone_number,
                            'is_candidate': self.user.is_candidate,
                            'is_hr': self.user.is_hr,
                            'is_employee': self.user.is_employee,
                            'email_validated': self.user.email_validated,
                            'profile_pic': p_pic,
                        }
                    except:
                        obj = {
                            'id': self.user.id,
                            'email': self.user.email,
                            'full_name': self.user.full_name,
                            'phone_number': self.user.phone_number,
                            'is_candidate': self.user.is_candidate,
                            'is_hr': self.user.is_hr,
                            'is_employee': self.user.is_employee,
                            'email_validated': self.user.email_validated,
                            'profile_pic': 'default.jpg',
                        }
                    data.update({'user': obj})
                    return data

                else:
                    msg = "You email is not verified.please check your email and verify to login"
            else:
                msg = "Your account is not active"
        else:
            msg = 'You are not Candidate.'

        raise serializers.ValidationError({'detail': msg})


class HRMCustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Admin Custom Authentication
    """
    # info = serializers.CharField(source='permission_user')
    non_field_errors = {
        'detail': 'Please verify your mail.'
    }
    default_error_messages = {
        'detail': 'Username or Password does not matched.'
    }

    def validate(self, attrs):
        data = super(HRMCustomTokenObtainPairSerializer, self).validate(attrs)
        if self.user.is_employee:
            if self.user.is_active:
                if self.user.email_validated:
                    request = self.context.get('request')
                    if 'default.jpg' in request.build_absolute_uri(str(self.user.profile_pic.url)):
                        p_pic = 'default.jpg'
                    else:
                        p_pic = request.build_absolute_uri(str(self.user.profile_pic.url))
                    try:
                        obj = {
                            'id': self.user.id,
                            'email': self.user.email,
                            'full_name': self.user.full_name,
                            'phone_number': self.user.phone_number,
                            'is_candidate': self.user.is_candidate,
                            'is_hr': self.user.is_hr,
                            'is_employee': self.user.is_employee,
                            'is_superuser': self.user.is_superuser,
                            'email_validated': self.user.email_validated,
                            'profile_pic': p_pic,
                        }
                    except:
                        obj = {
                            'id': self.user.id,
                            'email': self.user.email,
                            'full_name': self.user.full_name,
                            'phone_number': self.user.phone_number,
                            'is_candidate': self.user.is_candidate,
                            'is_hr': self.user.is_hr,
                            'is_employee': self.user.is_employee,
                            'is_superuser': self.user.is_superuser,
                            'email_validated': self.user.email_validated,
                            'profile_pic': 'default.jpg',
                        }
                    data.update({'user': obj})
                    return data

                else:
                    msg = "You email is not verified.please chek your email and verify to login"
            else:
                msg = "Your account is not active"
        else:
            msg = 'You are not Employee.'

        raise serializers.ValidationError({'detail': msg})


# User model Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.User.objects.all(),
                                    message='Already registered with this email address')],
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], \
                                     style={'input_type': 'password'})
    phone_number = serializers.CharField(max_length=15, min_length=9, required=True, style={'input_type': 'text'})

    class Meta:
        model = models.User
        fields = ('full_name', 'email', 'birthDate', 'gender', 'phone_number', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'birthDate': {'required': True},
            'password': {'write_only': True},
            'phone_number': {'write_only': True},

        }

    def create(self, validated_data):
        user = models.User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            birthDate=validated_data['birthDate'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],

        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = models.User
        fields = ['token']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    User profile update serializer
    """

    class Meta:
        model = models.User
        fields = ('full_name', 'birthDate', 'nationality', 'phone_number', 'gender', 'location', 'nid', 'profile_pic','signature_pic')
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
        instance.signature_pic = validated_data.get('signature_pic', instance.signature_pic)
        instance.save()
        return instance


class UserProfileCompletionPercentageSerializer(serializers.ModelSerializer):
    """
    Profile percentage progressbar
    """

    class Meta:
        model = models.User
        fields = ['id', 'full_name']


class EducationLevelSerializer(serializers.ModelSerializer):
    """
    Foreign key value for academic models data and filter automated data for the degree title.
    """

    class Meta:
        model = models.EducationLevelModel
        fields = '__all__'


class DegreeTitleSerializer(serializers.ModelSerializer):
    """
    Foreign key value for academic models data and filter automated data for the Degree title and education level
    wise filtering.
    """

    class Meta:
        model = models.DegreeTitleModel
        fields = '__all__'


class GroupOrSubjectSerializer(serializers.ModelSerializer):
    """
    Foreign key value for academic models data and filter automated data for the major group
    """

    class Meta:
        model = models.GroupOrSubjectModel
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):
    """
    Employee designation serializer
    """

    class Meta:
        model = models.UserDesignationModel
        fields = '__all__'


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


class CareerObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CareerObjectiveModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


# User Details serializer
class UserDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDepartmentModel
        fields = '__all__'


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SkillsModel
        fields = "__all__"


class UserSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(many=True,
                                          queryset=models.SkillsModel.objects.all(),
                                          slug_field='skillName')

    class Meta:
        model = models.UserSkillsModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        userSkills = models.UserSkillsModel.objects.create(**validated_data)
        userSkills.skills.add(*skills)
        return userSkills


class UserAcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserAcademicDetailsSerializer(serializers.ModelSerializer):
    educationLevel = EducationLevelSerializer()
    degreeTitle = DegreeTitleSerializer()

    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True}
        }


class UserCertificationsSerializer(serializers.ModelSerializer):
    expiry_date = serializers.CharField(source='certification_expiry_date', read_only=True)

    class Meta:
        model = models.UserCertificationsModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def to_representation(self, instance):
        data = super(UserCertificationsSerializer, self).to_representation(instance)
        expDate = data.get('expiry_date')
        if not expDate:
            data.pop('expiry_date')

        return data


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
User More info -> EmployeeInfoModel
Academic Information -> UserAcademicInfoModel
Certification Information -> UserCertificationsModel
Training Information -> UserTrainingModel
"""


class UserLoginDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'full_name', 'phone_number', 'is_candidate', 'is_employee', 'is_superuser', 'is_hr',
                  'email_validated', 'profile_pic']


class UserDetailsSerializer(serializers.ModelSerializer):
    careerObjective = CareerObjectiveSerializer(source='career_objective_user')
    academicInfo = UserAcademicDetailsSerializer(source='academic_info_user', many=True)
    certificationInfo = UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = UserJobPreferenceSerializer(source='job_preference_user', many=True)
    workExperience = UserWorkExperienceSerializer(source='working_experience_user', many=True)
    userSkills = UserSkillsSerializer(source='skills_user')

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


"""
Password change and reset section
Logout
"""


class ChangePasswordSerializer(serializers.Serializer):
    model = models.User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()
#
#     default_error_message = {
#         'bad_token': 'Token is expired or invalid'
#     }
#
#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs
#
#     def save(self, **kwargs):
#
#         try:
#             RefreshToken(self.token).blacklist()
#
#         except TokenError:
#             self.fail('bad_token')
