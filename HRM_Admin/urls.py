from django.urls import path
from HRM_Admin import views as hrm_admin_view
urlpatterns = [
    # path('add_new_employee_info/<application_id>/', hrm_admin_view.OnboardAnEmployeeView.as_view(),
    # name='new_employee_information_add'),
    path('add_new_employee_info/', hrm_admin_view.AddEmployeeInfoView.as_view(), name='add_new_employee_info'),
    path('employee_list/', hrm_admin_view.EmployeeInformationListView.as_view(), name='employee_list'),
    path('employee_info/<user_id>/', hrm_admin_view.EmployeeInformationView.as_view(), name='employee_information'),
    path('module_permission_access/<employee__user_id>/', hrm_admin_view.ManagePermissionAccessView.as_view(), name='module_permission_access'),
    path('employee_training/', hrm_admin_view.EmployeeTrainingView.as_view(), name='employee_training_information'),


]