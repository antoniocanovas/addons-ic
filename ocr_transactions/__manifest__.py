{
    'name': 'OCR transactions',
    'version': '12.0.6.3',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'contacts',
        'documents_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/document_ocr_tag.xml',
        'data/crea_lineas_factura.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
