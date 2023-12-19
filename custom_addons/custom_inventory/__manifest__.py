{
    'name': "Custom Inventory",
    'version': '16.0.0',
    'category': 'Sales',
    'summary': """ """,
    'description': """

    """,
    'depends': ['stock'],
    'website': "",
    'data': [
        'views/inventory_dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_inventory/static/src/js/inventory_dashboard.js',
            'custom_inventory/static/src/xml/inventory_dashboard.xml',
        ],
        'web.assets_frontend': [

        ],

    },
    'qweb': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': -1,
}
