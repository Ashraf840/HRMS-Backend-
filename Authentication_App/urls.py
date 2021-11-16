from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'authentication_app'
urlpatterns = [
    path('user_create/', views.ListCreateUserAPIView.as_view(), name='user_create'),
    path('user_create/<pk>', views.UserDetailAPIView.as_view(), name='user_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #JWT request
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#JWT api refresh

]
