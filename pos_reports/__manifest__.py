# -*- coding: utf-8 -*-
{
    'name': "IDT POS Reports",
    'summary': """
        Point of sale custom Reports""",
    'description': """
        Point of sale custom Reports
    """,
    'author': "IDT",
    'website': "https://www.idt.com",
    'category': 'Uncategorized',
    'version': '2.0',
    'depends': ['base','point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_reports.xml',
        'views/on_screen_reports.xml',
        'views/google_spreadsheets.xml',
        'views/company_summary.xml',
        'views/product_summary.xml',
        'views/sale_summary.xml',
        'views/category_summary.xml',
        'views/users_summary.xml',
        'views/customers_summary.xml',
        'views/payment_summary.xml',
        'views/dashboard.xml',

        'reports/periodic_sale_report.xml',
        'reports/daily_sales_details.xml',
        'reports/reports.xml',
        'wizard/periodic_sale_report_template.xml',
        'wizard/daily_sales_wizard.xml',


    ]
}