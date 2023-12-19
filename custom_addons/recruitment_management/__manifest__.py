{
    'name': 'Recruitment Management',
    'version': '15.0.0.2',
    'summary': 'Added functionality in the recruitment module',
    'sequence': 1,
    'category': 'Tools',
    'description': 'appraisal request form',
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'depends': ['base', 'hr_recruitment', 'hr'],
    'data': [
        "security/ir.model.access.csv",
        # "data/sequence.xml",
        "views/employee_salary_breakup.xml",
        "views/recruitment.xml",
        "views/employee.xml",
        "views/res_company.xml",
        "views/recruitment_review.xml",
        "views/recruitment_requisition.xml",
        'views/salary_based.xml',
        "reports/offer_letter_template_view.xml",
        "reports/appointment_letter_template_view.xml",
        "reports/menu.xml",
        "reports/confirmation_letter.xml",
        "reports/confirmation_letter_template.xml",
        'reports/salary_based_offer_letter.xml',
        'reports/bond_agreement_report.xml',
        'reports/for_ctc_based_offer_letter.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
