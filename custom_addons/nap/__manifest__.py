{
    'name': "Eenadu NAP",
    'version': '1.0.0',
    'category': 'Sales',
    'summary': """ """,
    'description': """

    """,
    'depends': ['sale', 'eenadu_reta', 'sales_circulation', 'eenadu_classified'],
    'website': "",
    'data': [
        'views/nap_view.xml',
        'views/inheriting_views.xml',
        'views/nap_orders_multi_state_view.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': -1,
}
