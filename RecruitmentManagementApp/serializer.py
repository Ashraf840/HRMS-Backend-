from rest_framework import serializers
# from rest_framework.utils.serializer_helpers import ReturnDict
from UserApp import serializer
from UserApp.models import User
from . import models


# Viewing all user information from admin panel
class AllUserDetailsSerializer(serializers.ModelSerializer):
    academicInfo = serializer.UserAcademicSerializer(source='academic_info_user', many=True)
    certificationInfo = serializer.UserCertificationsSerializer(source='certification_info_user', many=True)
    trainingInfo = serializer.UserTrainingExperienceSerializer(source='training_info_user', many=True)
    jobPreference = serializer.UserJobPreferenceSerializer(source='job_preference_user', many=True)
    userSkills = serializer.UserSkillsSerializer(source='skills_user')

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


# Job post Model Serializer -> Only for HR
class FilterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobApplyFilterQuestionModel
        fields = '__all__'


class JobPostSerializer(serializers.ModelSerializer):
    # filterQus = FilterQuestionSerializer()
    # filterQuestions = FilterQuestionSerializer(many=True)
    class Meta:
        model = models.JobPostModel
        exclude = ['user']
        extra_kwargs = {
            'user': {'read_only': True},

        }
        depth = 1


class OnlineTestLinkSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OnlineTestModel
        fields = '__all__'


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPostModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    # Multiple model data save at a time
    # def create(self, validated_data):
    #     # print(validated_data)
    #     jobData = validated_data.pop('jobInfo')
    #     # # onlineTestData = validated_data.pop('onlineTest')
    #     # question = validated_data.pop('filterQus')
    #     # progress = validated_data.pop('progressStatus')
    #     # print(question)
    #
    #     jobInfo = models.JobPostModel.objects.create(user_id=self.context['request'].user.id,
    #                                                  **jobData)
    #     # jobInfo.filterQuestions.add(*question)
    #     # jobInfo.jobProgressStatus.add(*progress)
    #     # print(jobInfo.filterQuestions.set(filterQus))
    #     onlineTest = models.OnlineTestModel.objects.create(jobInfo_id=jobInfo.id, **validated_data)
    #     return onlineTest


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobStatusModel
        fields = '__all__'


class PracticalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    # def create(self, validated_data):
    #     print(validated_data)
    #     jobData = validated_data.pop('jobInfo')
    #     validated_data.pop('cultural_test')
    #     validated_data.pop('analytical_test')
    #     # onlineTestData = validated_data.pop('onlineTest')
    #     # filterQus = jobData.pop('filterQuestions')
    #
    #     # jobInfo = models.JobPostModel.objects.create(user_id=self.context['request'].user.id, **jobData)
    #     # jobInfo.filterQuestions.set(filterQus)
    #     # onlineTest = models.OnlineTestModel.objects.create(jobInfo_id=jobInfo.id, **onlineTestData)
    #     practicalTest = models.PracticalTestModel.objects.create(jobInfo_id=jobData.id, **validated_data)
    #     return practicalTest


# Filter questions section

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDepartmentModel
        fields = '__all__'


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldTypeModels
        fields = '__all__'


class FilterQuestionAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilterQuestionAnswerModel
        fields = ['answer', ]


class FilterQuestionListSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer()
    fieldType = FieldTypeSerializer()
    answer = FilterQuestionAnsSerializer(source='job_apply_filter_question_answer')

    class Meta:
        model = models.JobApplyFilterQuestionModel
        fields = '__all__'


class FilterQuestionAnswerSerializer(serializers.ModelSerializer):
    question = FilterQuestionSerializer()

    class Meta:
        model = models.FilterQuestionAnswerModel
        fields = '__all__'

    def create(self, validated_data):
        question = validated_data.pop('question')
        filterQus = models.JobApplyFilterQuestionModel.objects.create(**question)
        qusAns = models.FilterQuestionAnswerModel.objects.create(question=filterQus, **validated_data)
        return qusAns

    def update(self, instance, validated_data):
        questionsData = validated_data.pop('question')
        instance.answer = validated_data.get('answer', instance.answer)
        instance.save()
        # questions = (instance.question)
        # print(questions)
        # questions = list(questions)
        # qus =questions.pop(0)
        questions = instance.question
        questions.question = questionsData.get('question', questions.question)
        questions.fieldType = questionsData.get('fieldType', questions.fieldType)
        questions.department = questionsData.get('department', questions.department)
        questions.save()
        return instance


class FilterQuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilterQuestionsResponseModelHR
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
        }


"""
Job progress functionality section
Job application functionality ,
step by step status changes
"""


class AppliedForJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }


class MyJobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'

        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }
        depth = 2

    def to_representation(self, instance):
        data = super(MyJobListSerializer, self).to_representation(instance)
        user = data.get('userId')
        user.pop('password')
        user.pop('is_staff')
        user.pop('is_active')
        user.pop('email_validated')
        user.pop('is_superuser')
        user.pop('is_employee')
        user.pop('is_hr')
        user.pop('is_candidate')
        user.pop('groups')
        user.pop('user_permissions')
        data.get('jobPostId').pop('filterQuestions')
        data.get('jobPostId').pop('user')

        return data


class CandidateStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            # 'jobProgressStatus': {'read_only': True},
            'jobPostId': {'read_only': True}
        }


class OnlineTestResponseSerializer(serializers.ModelSerializer):
    """
    Online test response will be stored here
    """

    class Meta:
        model = models.OnlineTestResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'appliedJob': {'read_only': True},
        }


class PracticalTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestResponseModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'appliedJob': {'read_only': True},
        }


class DocumentationSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentSubmissionModel
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'applied_job': {'read_only': True}
        }


class ReferenceInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferenceInformationModel
        # fields = '__all__'
        exclude = ['callRecord', 'is_verified', ]
        extra_kwargs = {
            'user': {'read_only': True},
            'applied_job': {'read_only': True},
            'refVerified': {'read_only': True}
        }
