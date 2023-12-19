# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Survey Form',
    'version': '0.1',
    'summary': 'Survey form',
    'sequence': 10,
    'description': """ """,
    'category': 'Survey',
    'depends': ['hr_recruitment','survey'],
    'data': [
        'view/view_suvery_update.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}