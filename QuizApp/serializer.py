from rest_framework import serializers
from . import models


class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSetModel
        fields = '__all__'


"""
Save data at two different models: 
question will save on QuestionSetModel
Answer will save on QuestionAnswerModel
"""


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSetSerializer()
    # author = serializers.ReadOnlyField(source='question_author')

    class Meta:
        model = models.QuestionAnswerModel
        fields = '__all__'

    def create(self, validated_data):
        questionData = validated_data.pop('question')
        question = models.QuestionSetModel.objects.create(**questionData)
        answer = models.QuestionAnswerModel.objects.create(question=question, **validated_data)
        return answer
