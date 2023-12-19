{
    'name': "Sales Person Target",
    'version': '16.0.0',
    'category': 'Sales',
    'summary': """ """,
    'description': """
        
    """,
    'depends': ['eenadu_classified',
                'eenadu_reta',
                'sale', 
                'sale_management', 
                'sale_stock', 
                'stock', 
                'contacts',
                'product'],
    'website': "",
    'data': [
        'security/ir.model.access.csv',
        'views/target_scheme_views.xml',
        'views/sale_person_target_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 1,
}
