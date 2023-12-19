# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Eenadu Classified',
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
        'sale','stock','sale_stock','sales_team','sales_circulation','eenadu_reta','account','product'
    ],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizards/reject_reason.xml',
        'wizards/update_and_approve.xml',
        'views/views.xml',
        'views/eenadu_reta_sale_inherit_views.xml',
        'views/ads_packages_view.xml',
        'views/classifieds_dashboard.xml',
        'views/classified_mgmt_dashboard.xml',
        'views/sale_category.xml',
        'views/scheduling_position_details_views.xml',
        'views/areas.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'eenadu_classified/static/src/js/classified_dashboard.js',
            'eenadu_classified/static/src/xml/classified_dashboard.xml',
            'eenadu_classified/static/src/js/classified_management_dashboard.js',
            'eenadu_classified/static/src/xml/classified_mgmt_dashboard.xml',
            'eenadu_classified/static/src/css/stylesheet.css',
            'eenadu_classified/static/src/css/mgmt_dashboard_ss.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}

