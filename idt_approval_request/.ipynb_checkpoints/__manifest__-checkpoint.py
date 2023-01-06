# -*- coding: utf-8 -*-
{
    'name': "Approval Request",

    'summary': """
        Approval Request for (e.g leave, loan etc)
        """,

    'description': """
        Approval Request for (e.g leave, loan etc)
    """,

    'author': "IDT",
    'website': "http://www.infinitedt.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Appproval',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','rating'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hr_approval_request_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
