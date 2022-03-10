from django.urls import path
from RecruitmentManagementApp import views

urlpatterns = [
    path('reference_verification_response/', views.ReferenceInformationResponseView.as_view()),
    path('reference_verification_questions/', views.ReferenceQuestionsRefView.as_view()),
]