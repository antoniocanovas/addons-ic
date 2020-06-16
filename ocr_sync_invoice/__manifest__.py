{
    'name': 'ocr sync invoice',
    'version': '12.10.0.6',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'ocr_transactions',
        'ase_replication_server',
    ],
    'data': [
        'views/views.xml',
        'views/res_company_ocr_manager.xml',
        'views/partner_credentials_ocr_manager.xml',
        'views/views_menu.xml'
    ],
    'installable': True,
}
