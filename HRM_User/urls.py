from django.urls import path
from HRM_User import views, models

urlpatterns = [
    path('training_response/', views.EmployeeTrainingResponseResultView.as_view(), name='employee_training_response'),

]
