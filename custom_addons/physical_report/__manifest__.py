# -*- coding: utf-8 -*-
{
    'name': "Physical Fitness Certificate",
    'version': '0.1',
    'summary': """Physical Fitness Certificate Report""",
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'sequence': -1,
    'depends': ['web', 'hr', 'base', 'website'],
    'auto_install': False,
    'installable': True,
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'views/hrms_wizard.xml',
        'report/template.xml',
        'views/wizard.xml',
        'report/joining_report.xml'
    ],
    'license': 'LGPL-3',
}
