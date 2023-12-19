{
    'name': "Eenadu Manufacturing",
    'version': '1.0.0',
    'category': 'MRP',
    'summary': """ """,
    'description': """
        
    """,
    'depends': ['sale', 'mrp', 'sales_circulation'],
    'website': "",
    'data': ['security/ir.model.access.csv',
             'views/mrp_eenadu.xml',
             'views/mrp_dashboard.xml',

             ],

    'assets': {
        'web.assets_backend': [
            'mrp_eenadu/static/src/js/mrp_dashboard.js',
            'mrp_eenadu/static/src/xml/mrp_dashboard.xml',
        ],
        'web.assets_frontend': [

        ],

    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': -1,
}
