from django.urls import path
from HRM_Admin import views as hrm_admin_view
urlpatterns = [
    # path('add_new_employee_info/<application_id>/', hrm_admin_view.OnboardAnEmployeeView.as_view(), name='new_employee_information_add'),
    path('add_new_employee_info/<application_id>/', hrm_admin_view.AddEmployeeInfoView.as_view(), name='add_new_employee_info'),

]