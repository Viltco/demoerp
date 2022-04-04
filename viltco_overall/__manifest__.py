# -*- coding: utf-8 -*-
{
    'name': "Viltco Overall",

    'summary': """
        This Module Contains Main Custom Functionalities of Viltco Portal""",

    'description': """
        This Module Contains Main Custom Functionalities of Viltco Portal
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'All',
    'version': '15.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'timesheet_grid', 'hr_timesheet', 'hr_payroll', 'hr_contract', 'hr'],

    # always loaded
    'data': [
        'data/server.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/payroll_views.xml',
        'views/project.xml',
        'views/working_hour.xml',
        'reports/invoice_report.xml',
    ],

}
