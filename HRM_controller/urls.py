from django.urls import path
from HRM_controller import views, models

urlpatterns = [
    path('survey_questions/', views.SurveyQuestionView.as_view(), name='survey_questions'),
    path('survey_user_response/', views.SurveyUserResponseView.as_view(), name='survey_user_response'),
    path('all_colleagues/', views.AllColleaguesView.as_view(), name='all_colleagues'),
    path('employee_evaluation_questions/', views.EmployeeEvaluationQuestionView.as_view(), name='employee_evaluation_questions'),
    path('employee_evaluation_create/<id>/', views.EmployeeEvaluationView.as_view(), name='employee_evaluation_create'),
    path('announcement/', views.AnnouncementView.as_view(), name='announcement'),
    path('notice/', views.NoticeView.as_view(), name='notice'),

    path('attendance_shift/', views.AttendanceShiftView.as_view(), name='attendance_shift'),
    path('attendance_shift/<id>/', views.AttendanceShiftView.as_view(), name='attendance_shift'),
    path('attendance_registration/', views.AttendanceRegistrationView.as_view(), name='attendance_registration'),
    path('attendance_registration/<id>/', views.AttendanceRegistrationView.as_view(), name='attendance_registration'),
]
