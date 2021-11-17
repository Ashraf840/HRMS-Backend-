from django.urls import path

from . import views

app_name = 'user_app'
urlpatterns = [
    path('create/', views.CustomUserCreate.as_view(), name="create_user"),
    path('<int:pk>/', views.UserDetails.as_view(), name="detail"),
    path('logout/', views.BlacklistTokenUpdateView.as_view(), name='blacklist'),


]
