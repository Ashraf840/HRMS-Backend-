from django.urls import path
# Importing Views from QuizApp
from QuizApp.views import QuestionAnswerSetView, SubmittedAnswerView, SubmittedAnswerListView, \
    FilterQuestionView
# importing Views from RecruitmentManagementApp views
from RecruitmentManagementApp.views import AllUserDetailView, JobPostView, AppliedForJobView, JobDescriptionView, \
    JobDescriptionUpdateDeleteView, JobListView, FilterQuestionResponseListView, FilterQuestionResponseView, \
    JobDataFilterView, \
    PracticalTestView, JobCreateView, OnlineTestResponseView, PracticalTestResponseView, \
    UpdateCandidateStatusView, MyJobListView, JobStatusView, PracticalTestForApplicantView, \
    OnlineTestResponseListView, DocumentSubmissionView, \
    DocumentSubmissionUpdateDeleteView, ReferenceInformationView, ReferenceInformationUpdateDeleteView
# importing Views from UserApp views
from UserApp.views import RegisterView, UserInfoListView, UserDetailView, \
    CustomTokenObtainPairView, UpdateAcademicInfoView, AddAcademicInfoView, \
    AddWorkExperienceView, UpdateWorkExpInfoView, AddCertificationsView, UpdateCertificationsView, \
    AddTrainingExperienceView, UpdateUserInfoView, UpdateTrainingExperienceView, VerifyEmailView, SkillsView, \
    AcademicInfoListView, WorkInfoListView, CertificationInfoListView, TrainingInfoListView, AddUserSkillsView, \
    HRMCustomTokenObtainPairView, DegreeTitleView, UserProfileCompletionPercentageView, EducationLevelView, \
    DepartmentView, UpdateUserSkillsView

from AdminOperationApp.views import AppliedUserDetailsView, AdminJobListView, OnlineTestLinkView, \
    RecruitmentAdminApplicantListView, AdminInterviewerListView, AdminAppliedCandidateOnlineResView, \
    SendPracticalTestView,  RecruitmentAdminGraphView, MarkingDuringInterviewView, AddEmployeeInfoDuringOnboardView, \
    FilterQuestionResponseListView, PracticalTestMarkUpdateView, RecruitmentPracticalTestResponseView,\
    InterviewTimeScheduleView, AdminDocumentVerificationView, GenerateAppointmentLetterView, AppointmentLetterInformationView


app_name = 'tfhrm_api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # new user registration
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),
    # email verification while creating new account
    path('users/', UserInfoListView.as_view(), name='users_list'),  # add new user from admin
    # Login url
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # Login url for user
    path('hrm_login/', HRMCustomTokenObtainPairView.as_view(), name='hrm-login_employee'),  # Login url for employee
    path('profile_completion_percentage/', UserProfileCompletionPercentageView.as_view(),
         name='profile_completion_percentage'),

    # employee
    path('users/<id>/', UserDetailView.as_view(), name='users'),  # user details
    path('update_profile/<pk>/', UpdateUserInfoView.as_view(), name='update_profile'),
    path('all_users/', AllUserDetailView.as_view(), name='all_users'),
    path('departments/', DepartmentView.as_view(), name='departments'),
    path('add_ac/', AddAcademicInfoView.as_view(), name='add_academics'),
    path('edu_level/', EducationLevelView.as_view(), name='education_level'),
    path('degree_titles/<educationLevel>/', DegreeTitleView.as_view(), name='degree_title_using_education_level'),
    path('update_ac/<user__id>/<id>/', UpdateAcademicInfoView.as_view(), name='update_academic'),
    path('add_ac_list/<id>/', AcademicInfoListView.as_view(), name='academic_info_list'),
    path('work_exp/', AddWorkExperienceView.as_view(), name='work_experiences'),
    path('up_work_exp/<user__id>/<id>/', UpdateWorkExpInfoView.as_view(), name='update_work_experiences'),
    path('work_exp_list/<id>/', WorkInfoListView.as_view(), name='work_experiences_list'),

    path('certifications/', AddCertificationsView.as_view(), name='certification'),
    path('certifications_list/<id>/', CertificationInfoListView.as_view(), name='certification_list'),
    path('up_certification/<user__id>/<id>/', UpdateCertificationsView.as_view(), name='update_certification'),

    path('training/', AddTrainingExperienceView.as_view(), name='training_exp'),
    path('training_list/<id>/', TrainingInfoListView.as_view(), name='training_exp_list'),
    path('up_training/<user__id>/<id>/', UpdateTrainingExperienceView.as_view(), name='update_training_exp'),
    path('add_user_skills/', AddUserSkillsView.as_view(), name='add_user_skills'),
    path('update_user_skills/<user_id>/', UpdateUserSkillsView.as_view(), name='update_user_skills'),
    # Hr operations
    path('add_skills/', SkillsView.as_view(), name="add_new_skills"),


    # for Candidate to Apply for Jobs
    path('job_post/', JobCreateView.as_view(), name='job_post_with_online_test_link'),
    # path('job_post/', JobPostView.as_view(), name='job_post_create'),
    path('job_status/', JobStatusView.as_view(), name='job_status'),
    path('job_list/<id>/', JobDescriptionView.as_view(), name='job_description'),
    path('job_update/<id>/', JobDescriptionUpdateDeleteView.as_view(), name='job_description_update_delete'),
    path('job_list/', JobListView.as_view(), name='job_list'),
    path('job_search/', JobDataFilterView.as_view(), name='job_search'),
    path('my_jobs/', MyJobListView.as_view(), name='my_jobs'),

    path('applied_job/', AppliedForJobView.as_view(), name='applied_for_jobs'),
    path('qus_ans/', QuestionAnswerSetView.as_view(), name='question_ans'),
    path('submit_ans/', SubmittedAnswerView.as_view(), name='submit_ans'),
    path('submitted_ans_list/', SubmittedAnswerListView.as_view(), name='submitted_ans_list'),

    # Filter question list
    path('filter_question/', FilterQuestionView.as_view(), name='filter_questions'),
    path('filter_question/<dep_id>/', FilterQuestionView.as_view(), name='filter_questions'),
    path('filter_question_res/', FilterQuestionResponseView.as_view(), name='filter_questions_response'),
    path('filter_question_res_list/', FilterQuestionResponseListView.as_view(), name='filter_questions_response_list'),

    # Online and practical Test Response model

    # change user current status
    path('online_test_link/<jobInfo>/', OnlineTestLinkView.as_view(), name='online_test_link'),
    path('online_test_res_list/<applied_job>/', OnlineTestResponseListView.as_view(), name='online_test_link'),

    path('online_test_res/<applied_job>/', OnlineTestResponseView.as_view(), name='online_test_response'),
    # path('online_test_res/', OnlineTestResponseView, name='online_test_response'),
    # path('practical_test/', PracticalTestView.as_view(), name='practical_test'),
    path('practical_test/<jobInfo>/', PracticalTestForApplicantView.as_view(), name='practical_test_for_a_job'),
    path('practical_test_res/<job_id>/', PracticalTestResponseView.as_view(), name='practical_test_response'),
    # Document submission by user
    path('documents_submit/<job_id>/', DocumentSubmissionView.as_view(), name='document_submission_add'),
    path('documents/<applied_job>/', DocumentSubmissionUpdateDeleteView.as_view(),
         name='document_submission_update_delete'),
    path('references_submit/<job_id>/', ReferenceInformationView.as_view(), name='references_information_add'),
    path('references/<applied_job>/', ReferenceInformationUpdateDeleteView.as_view(),
         name='references_information_update_delete'),

    #     Admin section URL
    path('send_practical_test/', SendPracticalTestView.as_view(), name='admin_send_practical_test'),
    path('update_status/<id>/', UpdateCandidateStatusView.as_view(), name='update_status'),
    path('practical_test_mark_update/<jobApplication>/', PracticalTestMarkUpdateView.as_view(),
         name='practical_test_mark_input_view'),
    path('recruitment_practical_test_res/', RecruitmentPracticalTestResponseView.as_view(),
         name='recruitment_practical_test_response'),
    path('recruitment_dashboard_applicant/', RecruitmentAdminApplicantListView.as_view(),
         name='recruitment_dashboard_applicant'),
    path('recruitment_dashboard/<year>/', RecruitmentAdminGraphView.as_view(), name='recruitment_dashboard_graph_jobs'),
    path('admin_job_list/', AdminJobListView.as_view(), name='admin_job_list'),
    path('filter_qus_res_list/<user_id>/<job_id>/', FilterQuestionResponseListView.as_view(),
         name='filter_qus_res_list_admin'),
    path('applicant_list_details/', AppliedUserDetailsView.as_view(), name='admin_applied_user_list'),
    path('admin_online_test_res_list/', AdminAppliedCandidateOnlineResView.as_view(),
         name='admin_online_test_response_list'),
    path('applicant_interview/', AdminInterviewerListView.as_view(), name='applicant_interviewer_list'),
    path('interview_schedule/', InterviewTimeScheduleView.as_view(), name='interview_time_schedule'),
    path('marking_during_interview/', MarkingDuringInterviewView.as_view(),
         name='marking_during_interview_interviewer'),
    # Document verification
    path('recruitment_documents_verification/<applied_job>/', AdminDocumentVerificationView.as_view(), name='document_verification_recruitment'),
    path('generate_appointment_letter/', GenerateAppointmentLetterView.as_view(), name='generate_appointment_letter_during_onboarding'),
    path('appointment_letter_details/<applied_job>/', AppointmentLetterInformationView.as_view(), name='appointment_letter_details_for_pdf'),
    # Update official email during onboard
    path('add_employee_info/<id>/', AddEmployeeInfoDuringOnboardView.as_view(),
         name='add_employee_info_during_onboard'),

]
