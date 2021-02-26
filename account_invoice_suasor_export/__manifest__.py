{
    'name': 'Account Invoice Suasor Export',
    'version': '12.0.0.0.2',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sql_export',
        'sql_request_abstract',
        'base_automation',
        'account_cancel',
    ],
    'data': [
        'views/suasor_invoice_views.xml',
        'data/create_suasor_invoice.xml',
        'data/export_suasor_invoice_sql.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
