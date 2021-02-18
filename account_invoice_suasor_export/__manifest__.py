{
    'name': 'Account Invoice Suasor Export',
    'version': '12.0.0.0.1',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'base_automation',
        'account',
    ],
    'data': [
        'views/suasor_invoice_views.xml',
        'data/create_suasor_invoice.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
