{
    'name': 'Hrms Nomination form Report',
    'summary': """This module allows to print the Nomination form report through wizard""",
    'version': '1.1',
    'author': 'Prime Minds',
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Management',
    'depends': ['base', 'website', 'web', 'hr'],
    'data': [
        'views/report.xml',
        'views/template.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': True,

}
