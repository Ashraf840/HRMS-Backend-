from rest_framework import serializers
from .models import User

# Authentication serializers
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'birth_date', 'date_joined', 'gender', 'password']
        extra_kwargs = {'password': {'write_only': True}}
