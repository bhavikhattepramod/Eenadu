# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo 16 Recurring Payment',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'category': 'Accounting',
    'version': '1.0.0',
    'description': """Odoo 16 Recurring Payment, Recurring Payment In Odoo, Odoo 16 Accounting""",
    'summary': 'Use recurring payments to handle periodically repeated payments',
    'sequence': 11,
    'depends': ['account'],
    'license': 'LGPL-3',
    'data': [
        'data/sequence.xml',
        'data/recurring_cron.xml',
        'security/ir.model.access.csv',
        'views/recurring_template_view.xml',
        'views/recurring_payment_view.xml'
    ],
    'images': ['static/description/banner.png'],
}
