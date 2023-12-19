# -*- coding: utf-8 -*-

{
    'name': 'GST Address Auto Complete - Odoo',
    'version':'16.0.1.0.1',
    'category':'Localization' ,
    'summary':'Auto populate customer address from GST number.',
    'description':'Auto populate customer address from GST number.' ,
    'website':'https://www.entrivistech.com',
    'author': 'Entrivis Tech Pvt. Ltd.',
    'depends':['l10n_in'],
    'support': 'hello@entrivistech.com',
    'images': ['static/description/Entrivis_GST.gif'],
    'data':[
            'views/res_partner_gst_address_view.xml',
            ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
