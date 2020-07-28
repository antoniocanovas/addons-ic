{
    'name': "Account Invoice Retention",
    'summary': """
        Asigna a la factura un asiento contable de retenciones creado a mano
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.0.0.1',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_invoice_form_retention.xml',
        'views/account_invoice_retention_template.xml',

    ],
    'installable': True,
}
