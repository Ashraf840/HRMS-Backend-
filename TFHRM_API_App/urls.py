from django.urls import path
# Importing Views from QuizApp
from QuizApp.views import QuestionAnswerSetView, SubmittedAnswerView, SubmittedAnswerListView, \
    FilterQuestionView
# importing Views from RecruitmentManagementApp views
from RecruitmentManagementApp.views import AllUserDetailView, JobPostView, AppliedForJobView, AppliedJobListView, \
    JobDescriptionView, JobListView, FilterQuestionResponseListView, FilterQuestionResponseView, JobDataFilterView, \
    PracticalTestView, JobPostOnlineView, OnlineTestResponseView,PracticalTestResponseView
# importing Views from UserApp views
from UserApp.views import RegisterView, UserInfoListView, UserDetailView, \
    CustomTokenObtainPairView, UpdateAcademicInfoView, AddAcademicInfoView, \
    AddWorkExperienceView, UpdateWorkExpInfoView, AddCertificationsView, UpdateCertificationsView, \
    AddTrainingExperienceView, UpdateUserInfoView, UpdateTrainingExperienceView, VerifyEmailView, SkillsView, \
    AcademicInfoListView, WorkInfoListView, CertificationInfoListView, TrainingInfoListView


app_name = 'tfhrm_api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('update_profile/<pk>', UpdateUserInfoView.as_view(), name='update_profile'),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),
    path('users/', UserInfoListView.as_view(), name='users_list'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('users/<id>/', UserDetailView.as_view(), name='users'),
    path('update_ac/<user__id>/<id>/', UpdateAcademicInfoView.as_view(), name='update_academic'),
    path('all_users/', AllUserDetailView.as_view(), name='all_users'),
    path('add_ac/', AddAcademicInfoView.as_view(), name='add_academics'),
    path('add_ac_list/<id>/', AcademicInfoListView.as_view(), name='academic_info_list'),
    path('work_exp/', AddWorkExperienceView.as_view(), name='work_experiences'),
    path('work_exp_list/<id>/', WorkInfoListView.as_view(), name='work_experiences_list'),
    path('up_work_exp/<user__id>/<id>/', UpdateWorkExpInfoView.as_view(), name='update_work_experiences'),

    path('certifications/', AddCertificationsView.as_view(), name='certification'),
    path('certifications_list/<id>/', CertificationInfoListView.as_view(), name='certification_list'),
    path('up_certification/<user__id>/<id>/', UpdateCertificationsView.as_view(), name='update_certification'),

    path('training/', AddTrainingExperienceView.as_view(), name='training_exp'),
    path('training_list/<id>/', TrainingInfoListView.as_view(), name='training_exp_list'),
    path('up_training/<user__id>/<id>/', UpdateTrainingExperienceView.as_view(), name='update_training_exp'),

    # Hr operations
    path('add_skills/', SkillsView.as_view(), name="add_new_skills"),
    # path('job_post/', JobPostView.as_view(), name='job_post_hr'),

    # for Candidate to Apply for Jobs
    path('applied_job/', AppliedForJobView.as_view(), name='applied_for_jobs'),
    path('job_list/<id>/', JobDescriptionView.as_view(), name='job_description'),
    path('applied_list/', AppliedJobListView.as_view(), name='applied_jobs_list'),
    path('job_list/', JobListView.as_view(), name='job_list'),
    path('job_search/', JobDataFilterView.as_view(), name='job_search'),
    # path('questions/',QuestionSetView.as_view(),name='question_set'),
    path('qus_ans/', QuestionAnswerSetView.as_view(), name='question_ans'),
    path('submit_ans/', SubmittedAnswerView.as_view(), name='submit_ans'),
    path('submitted_ans_list/', SubmittedAnswerListView.as_view(), name='submitted_ans_list'),
    path('job_post/', JobPostOnlineView.as_view(), name='job_post_with_online_test_link'),
    path('practical_test/', PracticalTestView.as_view(), name='practical_test'),

    # Filter question list
    path('filter_question/', FilterQuestionView.as_view(), name='filter_questions'),
    path('filter_question_res/', FilterQuestionResponseView.as_view(), name='filter_questions_response'),
    path('filter_question_res_list/', FilterQuestionResponseListView.as_view(), name='filter_questions_response_list'),

    # Online and practical Test Response model
    path('online_test_res/', OnlineTestResponseView.as_view(), name='online_test_response'),
    path('practical_test_res/', PracticalTestResponseView.as_view(), name='practical_test_response'),

]
