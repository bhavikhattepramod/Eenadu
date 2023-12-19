{
    'name': "Transport and Delivery Routes Portal",
    'version': '16.0.0',
    'category': 'Sales',
    'summary': """ """,
    'description': """
    """,
    'depends': ['custom_purchase', 'sale', 'sale_management', 'sale_stock', 'stock', 'contacts', 'web', 'account',
                'sales_team', 'base', 'sales_circulation'],
    'website': "",
    'data': [
        'security/ir.model.access.csv',
        'security/vendor_bill_groups.xml',
        'views/vendor_bill_view.xml',
        'views/transportation.xml',
        'views/transport_routes.xml',
        'views/transporter_routes.xml',
        'views/vehicles.xml',
        'views/stock_picking.xml',
        'views/driver_tracker.xml',
        'views/res_partner.xml',
        'views/transport_dashboard.xml',
        'reports/report_picking_entry.xml',
        'reports/report_entry.xml',
        'wizards/picking_transport_wizard.xml',
        'wizards/picking _transport_wizard_dup.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'transport_portal/static/src/js/transport_dashboard.js',
            'transport_portal/static/src/xml/transport_dashboard.xml',
        ],
        'web.assets_frontend': [

        ],

    },

    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': -1,
}
