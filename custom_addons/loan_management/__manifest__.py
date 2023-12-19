# -*- coding: utf-8 -*-
{
    'name': 'Loan Management',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Loan',
    'description': 'Loan Management',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'depends': ['base','om_hr_payroll','hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/loan_view.xml',
        'views/view_loan_ledger.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}