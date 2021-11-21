from django.urls import path

from HrManagementApp.views import AllUserDetailView
from UserApp.views import RegisterView, UserInfoListView, UserDetailView, UserAcademicInfoListView, \
    CustomTokenObtainPairView, UpdateAcademicInfoView, AddAcademicInfoView, \
    AddWorkExperienceView, UpdateWorkExpInfoView, AddCertificationsView, UpdateCertificationsView, \
    AddTrainingExperienceView, \
    UpdateTrainingExperienceView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserInfoListView.as_view(), name='users_list'),
    path('user_ac/<id>/', UserAcademicInfoListView.as_view(), name='user_ac_info'),
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
    # path('up/<id>/', views.UserDetailView.as_view()),
    # path('update_ac/<id>/', views..as_view()),

]
