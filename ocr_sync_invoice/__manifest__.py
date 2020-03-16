{
    'name': 'ocr sync invoice',
    'version': '12.0.2.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'account',
        'contacts',
        'documents_account',
        'ocr_transactions',
        'ase_replication_server',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
}
