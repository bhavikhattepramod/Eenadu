{
    'name': 'Employee Request Job Position Workflow',
    'version': '16.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Human Resources',
    'author': 'Prime Minds Consulting Pvt Ltd',
    'company': 'Prime Minds Consulting Pvt Ltd',
    'maintainer': 'Prime Minds Consulting Pvt Ltd',
    'website': "https://www.primeminds.co/",
    'depends': ['hr_recruitment', 'hr_skills', 'mail', 'recruit_inherit'],
    'data': [
        'security/ir.model.access.csv',
        'data/template_user_to_manger_views.xml',
        'data/template_manger_to_user_views.xml',
        'data/template_job_position_rejected_views.xml',
        'data/template_job_position_request_approved_views.xml',

        'views/job_position_request_sequence_views.xml',
        'views/job_position_request_views.xml',
        'views/hr_education.xml',
        'views/recruitment_dashboard.xml',

        'wizard/job_position_to_approve_views.xml',
        'wizard/job_position_hod_approve_views.xml',
        'wizard/job_position_approved_views.xml',
        'wizard/job_position_rejected_views.xml',
        'wizard/job_position_finance_approve_views.xml',
        'wizard/job_position_hr_approve.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dev_job_position_request/static/src/js/dashboard_supervisor.js',
            'dev_job_position_request/static/src/js/dashboard_hod.js',
            'dev_job_position_request/static/src/js/dashboard_finance.js',
            'dev_job_position_request/static/src/xml/dashboard_supervisor.xml',
            'dev_job_position_request/static/src/xml/dashboard_hod.xml',
            'dev_job_position_request/static/src/xml/dashboard_finance.xml',
            'dev_job_position_request/static/src/css/stylesheet.css',
        ],
    },
    'test': [],
    'css': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
