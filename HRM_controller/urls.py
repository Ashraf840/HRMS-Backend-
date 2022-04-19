from django.urls import path
from HRM_controller import views, models

urlpatterns = [
    # Survey Section
    path('survey_questions/', views.SurveyQuestionView.as_view(), name='survey_questions'),
    path('survey_user_response/', views.SurveyUserResponseView.as_view(), name='survey_user_response'),
    # Employee Evaluation Section
    path('all_colleagues/', views.AllColleaguesView.as_view(), name='all_colleagues'),
    path('employee_evaluation_questions/', views.EmployeeEvaluationQuestionView.as_view(), name='employee_evaluation_questions'),
    path('employee_evaluation_create/<id>/', views.EmployeeEvaluationView.as_view(), name='employee_evaluation_create'),
    # Announcement, Notice and Complain Section
    path('announcement/', views.AnnouncementView.as_view(), name='announcement'),
    path('notice/', views.NoticeView.as_view(), name='notice'),
    path('complain/', views.ComplainView.as_view(), name='complain'),
    path('complain_resolved/<id>/', views.ComplainResolvedView.as_view(), name='complain_resolved'),
    # Attendance Section
    path('holiday/', views.CreateHolidaysView.as_view(), name='holiday'),
    path('holiday/<id>/', views.CreateHolidaysView.as_view(), name='holiday'),
    path('attendance_shift/', views.AttendanceShiftView.as_view(), name='attendance_shift'),
    path('attendance_shift/<id>/', views.AttendanceShiftView.as_view(), name='attendance_shift'),
    path('attendance_registration/', views.AttendanceRegistrationView.as_view(), name='attendance_registration'),
    path('attendance_registration/<id>/', views.AttendanceRegistrationView.as_view(), name='attendance_registration'),
    path('attendance_log/', views.EmployeeAttendanceLogView.as_view(), name='employee_attendance_log'),
    # Employee Promotion Section
    path('employee_promotion/', views.EmployeePromotionView.as_view(), name='employee_promotion'),
    path('employee_promotion/<id>/', views.EmployeePromotionUpdateDeleteView.as_view(), name='employee_promotion'),
    #Temination Titel
    path('termination_title/', views.TerminationTitleView.as_view(), name='termination_title'),
    path('termination_title/<id>/', views.TerminationTitleUpdateDeleteView.as_view(), name='termination_title'),
    #Employee Termination
    path('employee_termination/', views.EmployeeTerminationView.as_view(), name='employee_termination'),
    path('employee_termination/<id>/', views.EmployeeTerminationUpdateDeleteView.as_view(), name='employee_termination'),
    #Employee Resignation
    path('employee_resignation/', views.EmployeeResignationView.as_view(), name='employee_resignation'),
    path('employee_resignation/<id>/', views.EmployeeResignationUpdateDeleteView.as_view(), name='employee_resignation'),
]
