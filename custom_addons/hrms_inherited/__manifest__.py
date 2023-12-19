{
    'name': 'hrmsinh',
   'version': '1.0',
   'summary ': 'details of ABC',
   'sequence': 10,
   'category': 'Productivity',
   'license':'LGPL-3',
   'depends': ['base', 'hr', 'Itax_calculation_master', 'recruitment_management','employee_self_service','hr_recruitment' ],
   'data': [
      'security/ir.model.access.csv',
      'views/hrms11.xml',
      'views/payroll.xml',
      'views/master_details_changes.xml',
      'views/insurance_policy_master.xml',
      'views/hr_recruit_changes.xml',
      'views/smart_button_payslip.xml',
      'wizards/payroll_generate_payslip.xml',
      'wizards/income_tax_xls.xml',
      'reports/xls.xml',
   ],
   'demo': [

   ],
   'qweb': [],
   'installable ': True,
   'application': True,
   'auto_install': False,

}

