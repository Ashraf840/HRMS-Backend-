from django.urls import path
from RecruitmentManagementApp import views

urlpatterns = [
    path('reference_verification_response/', views.ReferenceInformationResponseView.as_view(), name='reference_verification_response'),
    path('reference_verification_questions/', views.ReferenceQuestionsView.as_view()),
]