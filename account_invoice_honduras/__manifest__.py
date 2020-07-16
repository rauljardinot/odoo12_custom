{
    'name': 'Account Invoice Honduras',
    'version': '0.1',
    'description': 'Account Invoice Honduras',
    'category': 'app',
    'summary': '',
    'author': 'David Montero Crespo',
    'depends': ['web', 'mail','account','sale'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/ir_sequence_view.xml',
        'views/account_invoice.xml',
        'views/account_report.xml',
        'views/sale_order.xml',

    ]
}
