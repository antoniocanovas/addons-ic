{
    'name': 'Attachment Ocr2Invoice',
    'version': '12.0.1.0',
    'category': 'attachment',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'documents_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/document_ocr_tag.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'views/res_company_views.xml',
    ],
    'installable':True,
}
