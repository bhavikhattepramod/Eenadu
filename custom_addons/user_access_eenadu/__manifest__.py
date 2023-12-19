# -*- coding: utf-8 -*-

{
    'name': 'User Access New',
    'version': '16.0.2.0.1',
    'category': 'Purchase New',
    'description': 'Purchase New',
    'summary': 'Custom for purchase',
    'sequence': '1',
    'author': 'Pramod B K',
    'company': 'Pramod',
    'maintainer': 'Pramod',
    'website': "",
    'license': 'LGPL-3',
    'depends': ['product'],
    # 'live_test_url': 'https://www.youtube.com/watch?v=yA4NLwOLZms',
    'data': [
        'security/ir.model.access.csv',
        'security/access_rights.xml',
        'security/purchase_groups.xml',
        'security/purchase_new.xml',
        'views/notebook.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
