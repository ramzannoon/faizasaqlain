# -*- coding: utf-8 -*-
{
    'name': "Product Format",

    'summary': """
        Add New Menus In Product Under Configuration and Generate the Product Code """,

    'description': """
        Add New Menus In Product Under Configuration and Generate the Product Code
    """,

    'author': "IDT",
    'website': "http://www.idt.com",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '15.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/age_group_views.xml',
        'views/calender_season_views.xml',
        'views/product_accessories_view.xml',
        'views/product_component_view.xml',
        'views/product_year_views.xml',
        'views/product_template_views.xml',
    ],

}
