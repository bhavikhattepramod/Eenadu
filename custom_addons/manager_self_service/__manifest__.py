# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Manager Self Service',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Manager Approvals',
    'description': 'Manager Self Service',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'license': 'LGPL-3',
    'depends': ['recruit_inherit','hr_holidays','hr','base'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/onduty_form_manager.xml',
        'views/leave_form_manager.xml',
        'views/shift_form_manager.xml',
        'views/ontour_form_manager.xml',
        'views/rectification_form_manager.xml',
        'views/authorize_form_manager.xml',
        'views/lta_form_manager.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'manager_self_service/static/src/js/manager_dashboard.js',
            'manager_self_service/static/src/xml/manager_dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}