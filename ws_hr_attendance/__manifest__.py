# -*- coding: utf-8 -*-
{
    'name': "Attendance",

    'summary': """
        Attendance Customization
        """,

    'description': """
        Attendance Customization
        1- Attendance Rectification
    """,

    'author': "IDT",
    'website': "http://www.infintedt.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Attendance',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance','idt_approval_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/hr_attendance_wizard.xml',
        'views/hr_attendance_rectify_views.xml',
        'reports/hr_attendance_report.xml',
        'reports/hr_attendance_report_template.xml',
        'views/hr_attendance_template.xml',
        'views/hr_portal_attendance_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
