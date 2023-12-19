# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Eenadu Reports',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Eenadu Reports',
    'description': 'Eenadu Reports',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'license': 'LGPL-3',
    'depends': [
        'eenadu_reta', 'eenadu_classified','sales_circulation','product', 'sale'
    ],
    'demo': [],
    'data': ['security/ir.model.access.csv',
             'views/classified_dcr_report_view.xml',
             'views/reta_dcr_report_view.xml',
             'report/classified_dcr_report_.xml',
             'report/reta_dcr_report.xml',
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
