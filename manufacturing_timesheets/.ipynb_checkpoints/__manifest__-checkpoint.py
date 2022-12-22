# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Reports",
    'summary': """
       Manufacturing custom Reports""",
    'description': """
        Manufacturing Timesheets Reports
    """,
    'author': "IDT",
    'website': "https://www.idt.com",
    'category': 'Uncategorized',
    'version': '15.0.0.5',
    'depends': ['base', 'mrp','mrp_workorder','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/data_workcenter.xml',

        'views/manufacturing_timesheet.xml',
        'views/mrp_production.xml',
        'views/mrp_workcenter_productivity.xml',
        'views/mrp_workorder.xml',
        'views/sale_order_category.xml',
        'views/wip_report.xml',

        # 'wizard/create_bill.xml',

    ]
}
