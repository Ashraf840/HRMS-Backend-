from rest_framework import serializers
from HRM_controller import models


class SurveyQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SlugRelatedField(queryset=models.SurveyAnswerSheetModel.objects.all(), many=True,
                                           slug_field='answers')
    # answers = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.SurveyQuestionModel
        fields = '__all__'


class SurveyUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SurveyUserResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'is_answered': {
                'read_only': True
            },
            'months': {
                'read_only': True
            }
        }
