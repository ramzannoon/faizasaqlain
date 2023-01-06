# -*- coding: utf-8 -*-
{
    'name': "Outlet Internal Transfer",
    'summary': """
      Outlet Internal Transfer""",
    'description': """
      Outlet Internal Transfer
    """,
    'author': "IDT",
    'website': "https://www.idt.com",
    'category': 'Uncategorized',
    'version': '2.8',
    'depends': ['base', 'point_of_sale','stock'],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/outlet_internal_transfer.xml',

        'reports/individual_time_sheet.xml',
        'reports/outlet_wise_report.xml',
        'reports/reports.xml',
    ]
}