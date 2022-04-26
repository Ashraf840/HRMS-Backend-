from django.urls import path
from HRM_User import views, models

urlpatterns = [
    path('training_response/', views.EmployeeTrainingResponseResultView.as_view(), name='employee_training_response'),
    path('leave_request/', views.EmployeeLeaveRequestView.as_view(), name='employee_leave_request'),
    path('leave_request/<id>/', views.EmployeeLeaveRequestView.as_view(), name='employee_leave_request'),
    path('resignation_request/', views.EmployeeResignationRequestView.as_view(), name='employee_resignation_request'),
    #path('exit_answer/', views.EmployeeExitAnswersView.as_view(), name='employee_exit_questions'),

]
