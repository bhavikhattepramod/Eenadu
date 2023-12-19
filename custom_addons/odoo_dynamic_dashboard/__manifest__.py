# -*- coding: utf-8 -*-
{
    'name': "Odoo Dynamic Dashboard",
    'version': '16.0.1.0.0',
    'summary': """Create Configurable Dashboards Easily""",
    'description': """Create Configurable Dashboard Dynamically to get the information that are relevant to your business, department, or a specific process or need, Dynamic Dashboard, Dashboard, Dashboard Odoo""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'web','hide_menu'],
    'data': [
        'views/dashboard_view.xml',
        'views/dynamic_block_view.xml',
        'views/dashboard_menu_view.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_dynamic_dashboard/static/src/js/dynamic_dashboard.js',
            'odoo_dynamic_dashboard/static/src/scss/style.scss',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            'https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700',
            'odoo_dynamic_dashboard/static/src/xml/dynamic_dashboard_template.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
