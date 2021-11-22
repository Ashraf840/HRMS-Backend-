from django.urls import path
# importing Views from HrManagementApp views
from HrManagementApp.views import AllUserDetailView, JobPostView, AppliedForJobView, AppliedJobListView, \
    JobDescriptionView
# importing Views from UserApp views
from UserApp.views import RegisterView, UserInfoListView, UserDetailView, UserAcademicInfoListView, \
    CustomTokenObtainPairView, UpdateAcademicInfoView, AddAcademicInfoView, \
    AddWorkExperienceView, UpdateWorkExpInfoView, AddCertificationsView, UpdateCertificationsView, \
    AddTrainingExperienceView, \
    UpdateTrainingExperienceView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserInfoListView.as_view(), name='users_list'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('users/<id>/', UserDetailView.as_view(), name='users'),
    path('update_ac/<user__id>/<id>/', UpdateAcademicInfoView.as_view(), name='update_academic'),
    path('all_users/', AllUserDetailView.as_view(), name='all_users'),
    path('add_ac/', AddAcademicInfoView.as_view(), name='add_academics'),
    path('work_exp/', AddWorkExperienceView.as_view(), name='work_experiences'),
    path('up_work_exp/<user__id>/<id>/', UpdateWorkExpInfoView.as_view(), name='update_work_experiences'),

    path('certifications/', AddCertificationsView.as_view(), name='certification'),
    path('up_certification/<user__id>/<id>/', UpdateCertificationsView.as_view(), name='update_certification'),

    path('training/', AddTrainingExperienceView.as_view(), name='training_exp'),
    path('up_training/<user__id>/<id>/', UpdateTrainingExperienceView.as_view(), name='update_training_exp'),

    # Hr operations
    path('job_post/', JobPostView.as_view(), name='job_post_hr'),

    # for Candidate to Apply for Jobs
    path('applied_job/', AppliedForJobView.as_view(), name='applied_for_jobs'),
    path('job_des/<id>/', JobDescriptionView.as_view(), name='job_description'),
    path('applied_list/', AppliedJobListView.as_view(), name='applied_jobs_list'),
    # path('up_applied_job/<id>/', AppliedJobUpdateView.as_view(), name='Update_job_application'),

]