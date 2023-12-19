{
    'name': 'Eenadu Incentives',
    'version': '1.0.0',
    'category': 'Apps',
    'summary': 'Custom Incentives',
    'description': 'Reta Enhancement',
    'sequence': '10',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'license': 'LGPL-3',
    'depends': [
        'sale', 'eenadu_classified','hr','Itax_calculation_master','eenadu_reta','recruit_inherit','account',
    ],
    'demo': [],
    'data': [
             'security/ir.model.access.csv',
             'views/views.xml',
             'wizard/wizard_views.xml'

             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
