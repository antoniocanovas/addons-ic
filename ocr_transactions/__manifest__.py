{
    'name': 'OCR transactions',
    'version': '12.0.11.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'l10n_es_account_asset',
        'contacts',
        'dbcopy_post_actions',
        'queue_job_cron',
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
        'data/ocr_dbcopy_post_actions_job.xml',
        'data/dictionary_data.xml',
        'views/template.xml',
        'wizards/ocr_invoice_combination.xml',
    ],
    'installable': True,
}
