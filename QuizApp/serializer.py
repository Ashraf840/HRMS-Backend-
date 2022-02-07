from rest_framework import serializers
from . import models


# class FieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FieldTypeModels
#         fields = '__all__'


# class AnsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.QuestionAnswerModel
#         fields = '__all__'


# class QuestionSetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.QuestionSetModel
#         fields = '__all__'
#         # extra_kwargs ={
#         #     'author':{'read_only':True}
#         # }

    # """
    # Save data at two different models:
    # question will save on QuestionSetModel
    # Answer will save on QuestionAnswerModel
    # """


# class QuestionAnswerSerializer(serializers.ModelSerializer):
#     question = QuestionSetSerializer()
#
#     # author = serializers.ReadOnlyField(source='question_author')
#
#     class Meta:
#         model = models.QuestionAnswerModel
#         fields = '__all__'
#
#     def create(self, validated_data):
#         # print(validated_data)
#         questionData = validated_data.pop('question')
#         # print(validated_data)
#         question = models.QuestionSetModel.objects.create(**questionData)
#         answer = models.QuestionAnswerModel.objects.create(question=question, **validated_data)
#         return answer


# class SubmittedAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.SubmittedAnswerModel
#         fields = '__all__'
#
#         extra_kwargs = {
#             'user': {'read_only': True},
#             'correctAnswer': {'read_only': True}
#         }

#
# class SubmittedAnswerListSerializer(serializers.ModelSerializer):
#     correctAnswer = serializers.CharField(source='question.question_answer.qusAnswer', read_only=True)
#
#     class Meta:
#         model = models.SubmittedAnswerModel
#         fields = '__all__'
#
#         extra_kwargs = {
#             'user': {'read_only': True},
#             # 'correctAnswer': {'read_only': True}
#         }

#
# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.UserDepartmentModel
#         fields = '__all__'
#
#
# class FieldTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FieldTypeModels
#         fields = '__all__'
#
#
# class FilterQuestionAnsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FilterQuestionAnswerModel
#         fields = ['answer', ]
#
#
# class FilterQuestionListSerializer(serializers.ModelSerializer):
#     department = DepartmentSerializer()
#     fieldType = FieldTypeSerializer()
#     answer = FilterQuestionAnsSerializer(source='job_apply_filter_question_answer')
#
#     class Meta:
#         model = models.JobApplyFilterQuestionModel
#         fields = '__all__'
#
#
# class FilterQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.JobApplyFilterQuestionModel
#         fields = '__all__'
#
#
# class FilterQuestionAnswerSerializer(serializers.ModelSerializer):
#     question = FilterQuestionSerializer()
#
#     class Meta:
#         model = models.FilterQuestionAnswerModel
#         fields = '__all__'
#
#     def create(self, validated_data):
#         question = validated_data.pop('question')
#         filterQus = models.JobApplyFilterQuestionModel.objects.create(**question)
#         qusAns = models.FilterQuestionAnswerModel.objects.create(question=filterQus, **validated_data)
#         return qusAns
#
#     def update(self, instance, validated_data):
#         questionsData = validated_data.pop('question')
#         instance.answer = validated_data.get('answer', instance.answer)
#         instance.save()
#         # questions = (instance.question)
#         # print(questions)
#         # questions = list(questions)
#         # qus =questions.pop(0)
#         questions = instance.question
#         questions.question = questionsData.get('question', questions.question)
#         questions.fieldType = questionsData.get('fieldType', questions.fieldType)
#         questions.department = questionsData.get('department', questions.department)
#         questions.save()
#         return instance





# class FilterQuestionResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.FilterQuestionsResponseModel
#         fields = '__all__'
#
#         extra_kwargs = {
#             'user': {'read_only': True},
#
#         }
