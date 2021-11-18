from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('user_info/', views.UserInfoListView.as_view()),
    path('user/<pk>/', views.UserInfoApiView.as_view()),
    path('user_ac_info/<pk>/',views.UserAcademicInfoListView.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view()),
    path('logout/', views.LogoutView.as_view()),


]
