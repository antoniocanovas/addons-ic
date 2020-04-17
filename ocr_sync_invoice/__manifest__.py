{
    'name': 'ocr sync invoice',
    'version': '12.10.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'documents_account',
        'ocr_transactions',
        'ase_replication_server',
    ],
    'data': [
        'views/views.xml',
        'views/template.xml',
    ],
    'installable': True,
}
