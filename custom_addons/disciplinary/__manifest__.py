# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Disciplinary',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Disciplinary',
    'description': 'Employee Disciplinary',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'depends': ['mail','hr','base','employee_life_cycle','hr_attendance'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/disciplinary_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

