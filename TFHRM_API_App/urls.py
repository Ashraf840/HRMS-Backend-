from django.urls import path
from UserApp.views import RegisterView, UserInfoListView, UserDetailView, UserAcademicInfoListView, \
    UserAcademicInfoRetrieveView, CustomTokenObtainPairView, LogoutView, UpdateAcademicInfoView

from HrManagementApp.views import AllUserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('users/', UserInfoListView.as_view()),
    # path('user/<id>/', views.UserInfoApiView.as_view()),
    path('user_ac/<id>/', UserAcademicInfoListView.as_view()),
    # path('user_ac_update/<uid>/<id>/',views.UserAcademicInfoRetrieveView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('users/<id>/', UserDetailView.as_view()),
    path('update_ac/<user__id>/<id>/', UpdateAcademicInfoView.as_view()),
    path('all_users/', AllUserDetailView.as_view()),
    # path('up/<id>/', views.UserDetailView.as_view()),
    # path('update_ac/<id>/', views..as_view()),

]
