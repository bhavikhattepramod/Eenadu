
{
    'name': "One2many Search Widget",
    "version": "16.0.1.0.0",
    'summary': "Quick Search Feature For One2many Fields In Odoo",
    'description': 'One2Many Search Widget Helps the User to Search for a Word or Number. The One2many Rows Satisfying the '
               'Search will be Displayed and the Others get Hided.',
    "website": "https://primeminds.co",
    'company': 'Prime Minds consulting Pvt Ltd.',
    'category': 'Extra Tools',
    "author": "Murali G M and Altaf G",
    "license": "AGPL-3",
    'depends': ['base', 'web'],
    'assets': {
        'web.assets_backend': [
            '/one2many_search_widget/static/src/css/header.css',
            '/one2many_search_widget/static/src/js/one2manySearch.js',
            '/one2many_search_widget/static/src/xml/one2manysearch.xml',
        ],
    },
    "installable": True,
    "application": False,
    'images': ['static/description/banner.png'],
    'auto_install': False,
}
