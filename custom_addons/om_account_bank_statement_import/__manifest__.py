# -*- encoding: utf-8 -*-

{
    'name': 'Odoo 16 Account Bank Statement Import',
    'version': '16.0.2.0.0',
    'category': 'Accounting',
    'depends': ['account'],
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'maintainer': 'Odoo Mates',
    'license': 'LGPL-3',
    'description': """Generic Wizard to Import Bank Statements In Odoo 16 Community Edition.
(This module does include any CSV and XLSX type import format.)""",
    'data': [
        'security/ir.model.access.csv',
        'wizard/journal_creation.xml',
        'views/account_bank_statement_import_view.xml',
        'views/account_bank_statement_view.xml',
    ],
    'demo': [
        'demo/partner_bank.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}