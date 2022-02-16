from django.urls import path
from HRM_controller import views, models

urlpatterns = [
    path('survey_questions/', views.SurveyQuestionView.as_view(), name='survey_questions'),
    path('survey_user_response/', views.SurveyUserResponseView.as_view(), name='survey_user_response'),
]
