from django.urls import path
from HRM_Admin import views as hrm_admin_view
urlpatterns = [
    # Employee Onboard, new employee, employee list, information add section
    path('add_new_employee_info/', hrm_admin_view.AddEmployeeInfoView.as_view(), name='add_new_employee_info'),
    path('onboard_new_employee/', hrm_admin_view.OnboardAnEmployeeView.as_view(), name='onboard_new_employee'),
    path('employee_info_update/<user_id>/', hrm_admin_view.EmployeeInformationUpdateView.as_view(), name='employee_information_update'),
    path('employee_list/', hrm_admin_view.EmployeeInformationListView.as_view(), name='employee_list_search'),
    path('employee_info/<user_id>/', hrm_admin_view.EmployeeInformationView.as_view(), name='employee_information'),
    # set employee permission access section
    path('module_permission_access/<employee__user_id>/', hrm_admin_view.ManagePermissionAccessView.as_view(), name='module_permission_access'),
    # Employee training section
    path('employee_training/', hrm_admin_view.EmployeeTrainingView.as_view(), name='employee_training_information'),
    path('employee_training/<id>/', hrm_admin_view.EmployeeTrainingUpdateDeleteView.as_view(), name='employee_training_information_update_delete'),


]