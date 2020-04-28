{
    'name': 'OCR transactions',
    'version': '12.0.10.0.2',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'contacts',
        'documents_account',
        'dbcopy_post_actions',
        'queue_job_cron',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/document_ocr_tag.xml',
        'data/crea_lineas_factura.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'data/ocr_queue_job.xml',
        'data/ocr_dbcopy_post_actions_job.xml',
        'data/dictionary_data.xml',
    ],
    'installable': True,
}
