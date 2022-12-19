{
    'name': 'POS Sale Targets',
    'version': '13.0.0.3',
    'category': 'POS',
    "description": """ POS Sale Targets """,
    'author': "IDT",
    'website': 'http://www.infinitedt.com',
    'license': 'AGPL-3',
    'depends': [
        'base', 'point_of_sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_sale_targets.xml',
        'reports/pos_sale_targets.xml',
        'reports/goods_receive_notes.xml',

        'reports/reports.xml',
    ],
    'installable': True,
    'application': True,
}
