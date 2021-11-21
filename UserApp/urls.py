from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [

    # path('register/', views.RegisterView.as_view()),
    # path('user_info/', views.UserInfoListView.as_view()),
    # # path('user/<id>/', views.UserInfoApiView.as_view()),
    # path('user_ac_info/<id>/',views.UserAcademicInfoListView.as_view()),
    # # path('user_ac_update/<uid>/<id>/',views.UserAcademicInfoRetrieveView.as_view()),
    # path('login/', views.CustomTokenObtainPairView.as_view()),
    # path('logout/', views.LogoutView.as_view()),
    # path('user_detail/<id>/', views.UserDetailView.as_view()),
    # path('update_ac/<user__id>/<id>/', views.UpdateAcademicInfoView.as_view()),
    # # path('up/<id>/', views.UserDetailView.as_view()),
    # # path('update_ac/<id>/', views..as_view()),



]
