from rest_framework import serializers
from . import models


class AnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionAnswerModel
        fields = '__all__'


class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionSetModel
        fields = '__all__'
        # extra_kwargs ={
        #     'author':{'read_only':True}
        # }

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
        # print(validated_data)
        questionData = validated_data.pop('question')
        # print(validated_data)
        question = models.QuestionSetModel.objects.create(**questionData)
        answer = models.QuestionAnswerModel.objects.create(question=question, **validated_data)
        return answer


class SubmittedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubmittedAnswerModel
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
            'correctAnswer': {'read_only': True}
        }


class SubmittedAnswerListSerializer(serializers.ModelSerializer):
    correctAnswer = serializers.CharField(source='question.question_answer.qusAnswer', read_only=True)

    class Meta:
        model = models.SubmittedAnswerModel
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
            # 'correctAnswer': {'read_only': True}
        }


class FilterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobApplyFilterQuestionModel
        fields = '__all__'


# class FilterQuestionResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FilterQuestionsResponseModel
#         fields = '__all__'
#
#         extra_kwargs = {
#             'user': {'read_only': True},
#
#         }


