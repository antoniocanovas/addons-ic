{
    'name': 'OCR transactions',
    'version': '12.0.2.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'documents_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/document_ocr_tag.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
}
