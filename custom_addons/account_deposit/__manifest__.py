# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Eenadu account Deposit',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Custom Sales',
    'description': 'Sales Enhancement',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'license': 'LGPL-3',
    'depends': [
        'eenadu_reta', 'eenadu_classified','sales_circulation','product'
    ],
    'demo': [],
    'data': ['security/ir.model.access.csv',
             'views/account_deposit.xml',
             'views/deposit_wizard.xml',
             #'views/res_partner.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
