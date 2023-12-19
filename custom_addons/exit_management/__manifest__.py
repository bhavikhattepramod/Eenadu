# -*- coding: utf-8 -*-

{
    'name': 'HRMS - Exit Management',
    'version': '15.0.1.0 27-july',
    'summary': 'Handle the resignation process of the employee',
    'author': 'PMCL',
    'depends': ['base','hr', 'om_hr_payroll','mail','hr_work_entry'],
    'category': 'HR',
    'data': [
        'security/user_access.xml',
        'security/ir.model.access.csv',
        'data/hr_settlement_sequence.xml',
        'wizard/resignation_request_view.xml',
        # 'views/hr_employee.xml',
        'views/hr_leave_type.xml',
        'views/resignation_view.xml',
        'views/superannuation_relieving.xml',
        'views/notice_period_view.xml',
        'views/res_company_view.xml',
        'views/service_relieving.xml',
        'views/superannuation_intimation_letter.xml',
        'views/trainee_discharge_wizard.xml',
        'views/resigned_relieving.xml',
        'views/apprenticeship_resign_relieving.xml',
        'views/certificates_from_account_department.xml',
        'views/staff_canteen_certificates.xml',
        'views/knowledge_center_certificates.xml',
        'views/hr_dept.xml',
        'views/store_department.xml',
        'views/electronic_department.xml',
        'views/ushodaya_hr.xml',
        'views/app.xml',
        'views/clerancy.xml',
        'views/gslic_view.xml',
        'reports/reports.xml',
        'reports/settlement_slip.xml',
        'reports/relieving_letter.xml',
        'reports/exp_letter.xml',
        'reports/superannuations_relieving.xml',
        'reports/handover_form.xml',
        'reports/service_relievingreport.xml',
        'reports/superannuation_intimation_letter_report.xml',
        'reports/trainee_discharge_report.xml',
        'reports/resigned_relievingreport.xml',
        'reports/apprenticeship_resign_relieving.xml',
        'reports/certificates_from_account_department.xml',
        'reports/staff_canteen_certificates_report.xml',
        'reports/knowledge_center_certificates_report.xml',
        'reports/hr_dept_report.xml',
        'reports/store_dept_report.xml',
        'reports/electronic.xml',
        'reports/ushodaya_hr_report.xml',
        'reports/appreport.xml',
        'reports/clerancy_reports.xml',
        'reports/gslic_report.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
