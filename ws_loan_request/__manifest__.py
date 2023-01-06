# -*- coding: utf-8 -*-
{
    'name': "Loan",

    'summary': """
        Loan
        """,

    'description': """
        Loan Request
    """,

    'author': "IDT",
    'website': "http://www.infinitedt.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Employees',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_payroll','de_hr_payroll_policy','idt_approval_request'],

    # always loaded
    'data': [
        'data/hr_loan_seq.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hr_loan_views.xml',
        'views/hr_employee_views.xml',
        'views/advance_against_expense_views.xml',
        'views/hr_loan_type_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
