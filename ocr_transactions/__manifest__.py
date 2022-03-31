{
    'name': 'OCR transactions',
    'version': '14.0.4.1.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'l10n_es_account_asset',
        'queue_job',
        'partner_credentials',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/crea_lineas_factura.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/views_account_invoice.xml',
        'data/ocr_queue_job.xml',
        'data/default_ocr_user.xml',
        'data/dictionary_data.xml',
        'data/pasar_factura_compra.xml',
        'data/send_through.xml',
        'views/template.xml',
        'wizards/ocr_invoice_combination.xml',
    ],
    'installable': True,
}
