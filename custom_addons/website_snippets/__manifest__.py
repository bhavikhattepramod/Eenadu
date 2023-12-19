{
    'name': 'Custom Website',
    'summary': """New access groups are added in this module""",
    'version': '16.0.0.1 10-june',
    'description': """New access groups are added in this module""",
    'author': 'PMCS',
    "license": "AGPL-3",
    'sequence': 10,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Tools',
    'depends': ['web','portal','website'],
    'data': [
        'views/login_new.xml'

    ],
'assets': {
        'web.assets_backend': [
            'website_snippets/static/css/stylesheet.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
