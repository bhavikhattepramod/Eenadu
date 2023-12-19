# -*- coding: utf-8 -*-

{
    'name': 'Send SMS',
    'version': '16.0.1.0.1',
    'category': 'Localization',
    'summary': 'Send Custom Messages to Customer',
    'description': 'Send Custom Messages to Customer',
    'website': 'https://www.primeminds.co',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'depends': ['sale','eenadu_reta','nap'],
    'support': 'https://www.primeminds.co',
    'data': [
        'security/ir.model.access.csv',
        'wizard/otp_verification.xml',
        'views/sms_custom_fields.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
