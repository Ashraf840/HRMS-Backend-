from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from UserApp.models import User, UserDepartmentModel, EmployeeInfoModel, UserDesignationModel
from . import models
from django.db.models import Q
from RecruitmentManagementApp.models import UserJobAppliedModel, JobPostModel, OnlineTestModel, OnlineTestResponseModel, \
    FilterQuestionsResponseModelHR, DocumentSubmissionModel
from RecruitmentManagementApp.serializer import OnlineTestResponseSerializer, PracticalTestResponseSerializer, \
    JobStatusSerializer, FilterQuestionSerializer, ReferenceInformationSerializer


class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartmentModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Return user basic information
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'profile_pic', 'phone_number', 'nid', 'nationality', 'location']


class InterviewerSerializer(serializers.ModelSerializer):
    """
    Return Interviewer basic information and designation
    """
    designation = serializers.CharField(source='user_info_user.designation')

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'designation']


class JobSerializer(serializers.ModelSerializer):
    # filterQus = FilterQuestionSerializer()

    class Meta:
        model = JobPostModel
        fields = ['id', 'jobTitle', 'jobType', 'shift']


class AdminOnlineTestLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineTestModel
        fields = '__all__'
        extra_kwargs = {
            'jobInfo': {'read_only': True}
        }


class SendPracticalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestUserModel
        fields = '__all__'
        extra_kwargs = {
            # 'user': {'read_only': True},
            # 'practicalTestInfo': {'read_only': True}
        }


class RecruitmentNewApplicantSerializer(serializers.ModelSerializer):
    """
    New applicant list serializer
    """
    userId = UserSerializer()
    jobPostId = JobSerializer()
    jobProgressStatus = JobStatusSerializer()

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'


class MarkingDuringInterviewSerializer(serializers.ModelSerializer):
    """
    Interviewer will mark Candidate During Interview based on few criteria.
    """

    # interviewer = InterviewerSerializer()

    class Meta:
        model = models.MarkingDuringInterviewModel
        fields = '__all__'

        extra_kwargs = {
            'interviewer': {'read_only': True}
        }


class MarkingListDuringInterviewSerializer(serializers.ModelSerializer):
    """
    Interview feedback List serializer for recruitment admin panel interview
    """
    interviewer = InterviewerSerializer()

    class Meta:
        model = models.MarkingDuringInterviewModel
        fields = '__all__'

        extra_kwargs = {
            'interviewer': {'read_only': True}
        }


class AdminDashboardSerializer(serializers.ModelSerializer):
    """
    Admin Dashboard serializer
    return Job applied information
    and manually
    """
    jobPostId = JobSerializer()
    userId = UserSerializer()
    jobProgressStatus = JobStatusSerializer()

    # print(jobPostId)
    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        # depth = 1

    # def to_representation(self, instance):
    #     data = super(AdminDashboardSerializer, self).to_representation(instance)
    #     jobInfo = data.get('jobPostId')
    #     # print(jobInfo)
    #     # jobInfo.pop('id')
    #     # jobInfo.pop('filterQuestions')
    #     # jobInfo.pop('jobProgressStatus')
    #     # jobInfo.pop('is_active')
    #     # jobInfo.pop('jobDescription')
    #     # jobInfo.pop('jobType')
    #     # jobInfo.pop('lastUpdated')
    #     # jobInfo.pop('postDate')
    #     # jobInfo.pop('department')
    #     # jobInfo.pop('vacancies')
    #
    #     return data


class AdminJobListSerializer(serializers.ModelSerializer):
    """
    All posted job will be visible here and total no of applicant will be shown here
    """

    total_count = serializers.SerializerMethodField('_checked')

    def _checked(self, filters):
        total = getattr(filters, 'total_applied')
        return total

    # filterQuestions = FilterQuestionSerializer(many=True)

    class Meta:
        model = JobPostModel
        fields = '__all__'


class AppliedUserDetailsSerializer(serializers.ModelSerializer):
    """
        Applicant list will be visible here in admin dashboard.
    """
    userId = UserSerializer()
    jobPostId = JobSerializer()

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        extra_kwargs = {
            'userId': {'read_only': True},
            'jobProgressStatus': {'read_only': True}
        }
        # depth = 1


class FilterQuestionResponseListSerializer(serializers.ModelSerializer):
    questions = FilterQuestionSerializer()

    class Meta:
        model = FilterQuestionsResponseModelHR
        fields = '__all__'


class AdminAppliedCandidateOnlineResSerializer(serializers.ModelSerializer):
    """
    Online test response list and user info for admin panel online test dashboard
    """

    class Meta:
        model = OnlineTestResponseModel
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        data = super(AdminAppliedCandidateOnlineResSerializer, self).to_representation(instance)
        info = data.get('user')
        info.pop('password')
        info.pop('is_staff')
        info.pop('is_active')
        info.pop('email_validated')
        info.pop('is_superuser')
        info.pop('is_employee')
        info.pop('is_hr')
        info.pop('is_candidate')
        info.pop('groups')
        info.pop('user_permissions')
        info.pop('date_joined')
        data.get('appliedJob').pop('userId')
        # data.get('appliedJob').get('jobPostId').pop('user')

        return data


class TestOnlineTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineTestResponseModel
        fields = '__all__'


class TestAdminAppliedCandidateOnlineResSerializer(serializers.ModelSerializer):
    onlineTestResponse = TestOnlineTestResponseSerializer(source='job_applied_online_response', many=True)
    userId = UserSerializer()
    jobProgressStatus = JobStatusSerializer()

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'

    def to_representation(self, instance):
        data = super(TestAdminAppliedCandidateOnlineResSerializer, self).to_representation(instance)
        # print(data)
        info = data.get('onlineTestResponse')
        # print(info)
        # response = []
        # print(len(info))
        if len(info) == 0:
            data.clear()
        return data


class PracticalTestMarkInputSerializer(serializers.ModelSerializer):
    """
    Practical Test Mark input serializer
    """

    class Meta:
        model = models.PracticalTestMarkInputModel
        fields = '__all__'

        extra_kwargs = {
            'markAssignBy': {'read_only': True},
            'jobApplication': {'read_only': True}
        }


class JobStatusRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobAppliedModel
        fields = ''


class JobAppliedUserSerializer(serializers.ModelSerializer):
    jobPostId = JobSerializer()
    jobProgressStatus = JobStatusSerializer()

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'


class RecruitmentPracticalTestResponseSerializer(serializers.ModelSerializer):
    """
    Recruitment practical test response and mark serializer
    """
    user = UserSerializer()
    practicalMark = PracticalTestMarkInputSerializer(source='appliedJob.practical_test_application')
    appliedJob = JobAppliedUserSerializer()

    class Meta:
        model = models.PracticalTestResponseModel
        fields = '__all__'


class InterviewTimeScheduleSerializer(serializers.ModelSerializer):
    """
    Interview time scheduling
    """
    interviewer = serializers.SlugRelatedField(queryset=UserDesignationModel.objects.filter(Q(designation='CEO') |
                                                                                            Q(designation='HR') |
                                                                                            Q(designation='PM') |
                                                                                            Q(designation='GM')),
                                               slug_field='designation')

    # scheduleBy = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='full_name')

    class Meta:
        model = models.InterviewTimeScheduleModel
        fields = '__all__'

        extra_kwargs = {
            'scheduleBy': {'read_only': True}
        }


class AdminInterviewerListSerializer(serializers.ModelSerializer):
    """
    selected user for interview. will show online,practical test result will show
    """
    onlineTest = OnlineTestResponseSerializer(source='job_applied_online_response', many=True)
    practicalTest = PracticalTestResponseSerializer(source='job_applied_practical_response')
    practicalTestMarks = PracticalTestMarkInputSerializer(source='practical_test_application')
    interviewFeedback = MarkingListDuringInterviewSerializer(source='applied_job_user_applied_model', many=True)
    interviewSchedule = InterviewTimeScheduleSerializer(source='application_id_applied_job', many=True)
    userId = UserSerializer()
    jobProgressStatus = JobStatusSerializer()
    jobPostId = JobSerializer()

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'
        # depth = 1

    # def to_representation(self, instance):
    #     data = super(AdminInterviewerListSerializer, self).to_representation(instance)
    #     # serializer.get('userId').pop('password')
    #     user = data.get('userId')
    #     user.pop('password')
    #     user.pop('is_staff')
    #     user.pop('is_active')
    #     user.pop('email_validated')
    #     user.pop('is_superuser')
    #     user.pop('is_employee')
    #     user.pop('is_hr')
    #     user.pop('is_candidate')
    #     user.pop('groups')
    #     user.pop('user_permissions')
    #     user.pop('date_joined')
    #
    #     data.get('jobPostId').pop('filterQuestions')
    #     return data


class AddEmployeeInfoDuringOnboardSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = EmployeeInfoModel
        fields = ['id', 'user', 'salary', 'designation', 'department', 'shift', 'email']
        # fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


"""
==================Salary section==================
"""


class FinalSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FinalSalaryNegotiationModel
        fields = '__all__'
        extra_kwargs = {
            'assignedBy': {'read_only': True}
        }


"""
==================Document section==================
"""


class OnlineTestResSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineTestResponseModel
        fields = '__all__'


class PracticalTestResSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PracticalTestMarkInputModel
        fields = '__all__'


class HrFeedbackInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MarkingDuringInterviewModel
        fields = '__all__'


class SelectedForDocumentationSerializer(serializers.ModelSerializer):
    userId = UserSerializer()
    # applied_job = JobAppliedUserSerializer()
    onlineTestRes = OnlineTestResSerializer(source='job_applied_online_response', many=True)
    practicalTestRes = PracticalTestResSerializer(source='practical_test_application')
    feedback = HrFeedbackInterviewSerializer(source='applied_job_user_applied_model', many=True)
    jobProgressStatus = JobStatusSerializer()

    class Meta:
        model = UserJobAppliedModel
        fields = '__all__'


class DocumentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobAppliedModel
        fields = ['id']


class AdminDocumentVerificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    references = ReferenceInformationSerializer(source='applied_job.references_submission_applied_job', many=True)

    class Meta:
        model = DocumentSubmissionModel
        fields = '__all__'


class AdminDocumentVerifySerializer(serializers.ModelSerializer):
    # comments = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = DocumentSubmissionModel
        fields = ['is_verified']


class CommentsOnDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentsOnDocumentsModel
        fields = '__all__'


class GenerateAppointmentLetterSerializer(serializers.ModelSerializer):
    """
    On-boarding section for candidate where admin will set appointment letter and others documents
    """

    class Meta:
        model = models.GenerateAppointmentLetterModel
        fields = '__all__'
        # extra_kwargs = {
        #     'applicationId': {'read_only': True}
        # }
