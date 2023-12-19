# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    "name": "Code Backend Theme V16",
    "description": """Minimalist and elegant backend theme for Odoo 16, Backend Theme, Theme""",
    "summary": "Code Backend Theme V16 is an attractive theme for backend",
    "category": "Themes/Backend",
    "version": "16.0.1.0.0",
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    "depends": ['base', 'web', 'mail'],
    "data": [
        'views/layout.xml',
        'views/icons.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'code_backend_theme/static/src/xml/styles.xml',
            'code_backend_theme/static/src/xml/top_bar.xml',
            'code_backend_theme/static/src/scss/theme_accent.scss',
            'code_backend_theme/static/src/scss/navigation_bar.scss',
            'code_backend_theme/static/src/scss/datetimepicker.scss',
            'code_backend_theme/static/src/scss/theme.scss',
            'code_backend_theme/static/src/scss/sidebar.scss',
            'code_backend_theme/static/src/js/chrome/sidebar_menu.js',
            'code_backend_theme/static/src/js/fields/colors.js',

        ],
        'web.assets_frontend': [
            'code_backend_theme/static/src/scss/login.scss',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'license': 'LGPL-3',
    'pre_init_hook': 'test_pre_init_hook',
    'post_init_hook': 'test_post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
