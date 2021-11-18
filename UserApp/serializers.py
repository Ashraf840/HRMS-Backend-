from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, UserInfoModel
from . import models

# class UserInfoModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInfoModel
#         fields= '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # info = serializers.CharField(source='permission_user')
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        obj = {
            'email': self.user.email,
            # 'fullName': self.user.full_name,
            'id': self.user.id,
            # 'gender': self.user.gender,

        }
        data.update({'obj': obj})

        return data


class UserAcademicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserSerializer(serializers.ModelSerializer):
    # info = serializers.RelatedField(many=True)
    user = UserInfoSerializer()
    # userAcademicInfo = UserAcademicInfoSerializer()

    class Meta:
        model = UserInfoModel
        fields = '__all__'
        # exclude = ['password']
        depth = 1
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


# User Academic info serializer
class UserAcademicInfoSerializer(serializers.ModelSerializer):
    # info = serializers.RelatedField(many=True)
    user = UserInfoSerializer()
    # userAcademicInfo = UserAcademicInfoSerializer()

    class Meta:
        model = models.UserAcademicInfoModel
        fields = '__all__'
        # exclude = ['password']
        depth = 1