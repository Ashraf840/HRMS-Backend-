from django.urls import path

from . import views

app_name = 'user_app'
urlpatterns = [
    path('create/', views.CustomUserCreate.as_view(), name="create_user"),
    path('', views.UserListView.as_view(), name="list"),
    path('<int:pk>/', views.UserDetailView.as_view(), name="detail"),
    path('logout/', views.BlacklistTokenUpdateView.as_view(), name='blacklist'),


]
