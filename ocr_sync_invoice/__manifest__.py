{
    'name': 'ocr sync invoice',
    'version': '12.0.1.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'contacts',
        'documents_account',
        'ocr_transactions',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
}
