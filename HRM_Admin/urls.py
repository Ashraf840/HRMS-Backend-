from django.urls import path
from HRM_Admin import views as hrm_admin_view

urlpatterns = [
    # Employee Onboard, new employee, employee list, information add section
    path('add_new_employee_info/', hrm_admin_view.AddEmployeeInfoView.as_view(), name='add_new_employee_info'),
    path('onboard_new_employee/', hrm_admin_view.OnboardAnEmployeeView.as_view(), name='onboard_new_employee'),
    path('employee_list/', hrm_admin_view.EmployeeInformationListView.as_view(), name='employee_list_search'),
    path('employee_filter/',hrm_admin_view.EmployeeInformationFilterView.as_view(),name='employee_filter'),
    path('employee_info/<user_id>/', hrm_admin_view.EmployeeInformationView.as_view(), name='employee_information'),
    path('employee_info_update/<user_id>/', hrm_admin_view.EmployeeInformationUpdateView.as_view(),
         name='employee_information_update'),
    path('employee_bank_info/', hrm_admin_view.EmployeeBankInformationView.as_view(), name='employee_bank_info_add'),
    path('employee_bank_info/<id>/', hrm_admin_view.EmployeeBankInformationUpdateView.as_view(),
         name='employee_bank_info_update_delete'),
    path('employee_documents/<user>/', hrm_admin_view.EmployeeDocumentsListView.as_view(),
         name='employee_documents_list'),
    # set employee permission access section
    path('module_permission_access/<employee__user_id>/', hrm_admin_view.ManagePermissionAccessView.as_view(),
         name='module_permission_access'),
    # Employee training section
    path('employee_training/', hrm_admin_view.EmployeeTrainingView.as_view(), name='employee_training_information'),
    path('employee_training/<id>/', hrm_admin_view.EmployeeTrainingUpdateDeleteView.as_view(),
         name='employee_training_information_update_delete'),
    # Department and Designation
    path('dept_head_list/', hrm_admin_view.EmployeeForDeptHeadView.as_view(), name='department_head_list'),
    path('depratments/', hrm_admin_view.DepartmentsView.as_view(), name='departments'),
    path('depratments/<id>/', hrm_admin_view.DepartmentUpdateView.as_view(), name='departments_update'),
    path('designations/', hrm_admin_view.DesignationsView.as_view(), name='designations'),
    path('designations/<id>/', hrm_admin_view.DesignationUpdateView.as_view(), name='designations_update'),
     #Employee Resignation
    path('employee_resignation/', hrm_admin_view.EmployeeResignationView.as_view(), name='employee_resignation'),
    path('employee_resignation/<id>/', hrm_admin_view.EmployeeResignationUpdateDeleteView.as_view(), name='employee_resignation'),
    # Document
    path('employee_documents_all/<id>/',hrm_admin_view.EmployeeDocumentUpdateDeleteView.as_view(),name='employee_documents_all'),
    # path('employee_document_list/',hrm_admin_view.EmployeeDocumentListView.as_view(),name='employee_document_list'),

    # Paid invoices
    path('paid_invoice/',hrm_admin_view.PaidInvoiceListView.as_view(),name='paid_invoice'),
    path('paid_invoice/<id>/',hrm_admin_view.PaidInvoiceDeleteApiView.as_view(),name='paid_invoice_delete'),
    # Warrenty File
    path('warranty_list/',hrm_admin_view.WarrantyListApiView.as_view(),name='warranty_list'),
    path('warranty_list/<id>/',hrm_admin_view.WarrentyDocumentListDeleteApiView.as_view(),name='warranty_delete'),
    # Salary sheet of employee
    path('employee_salary_sheets/',hrm_admin_view.SalaryCreateListApiView.as_view(),name='salary_sheet'),
#     path('employee_salary_sheet_new/',hrm_admin_view.NewSalarySheet.as_view(),name='salary_sheet'),
#     path('new_new/',hrm_admin_view.testView.as_view(),name='new_new'),
#     path('test/',hrm_admin_view.testView.as_view(),name='test'),
]