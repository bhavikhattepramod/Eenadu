# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Purchase',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Custom Purchase',
    'description': 'Purchase Enhancement',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'license': 'LGPL-3',
    'depends': [
        'purchase','stock','purchase_stock',
    ],
    'demo': [],
    'data': [
        'security/newsprint_purchase_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        # 'views/res_users_views.xml',
        'views/custom_purchase_views.xml',
        'views/claim_insurance_international_views.xml',
        'views/international_policy_views.xml',
        'views/domestic_policy_views.xml',
        'views/claim_insurance_domestic_views.xml',
        'views/ship_onboard_views.xml',
        'views/shipment_distribution_views.xml',
        'views/stock_lot_views.xml',
        'views/stock_move_line_views.xml',
        'views/stock_picking_views.xml',
        'views/newsprint_manufacturer_views.xml',
        'views/stock_move_views.xml',
        # 'views/stock_warehouse_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}

