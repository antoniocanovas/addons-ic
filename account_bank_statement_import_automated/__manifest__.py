# -*- encoding: utf-8 -*-
{
    'name': 'Account Bank Statement Import Automated',
    'category': 'Accounting',
    'version': '12.0.0.0.1',
    'depends': ['account'],
    'description': """ Upload multiple documents n43 formated """,
    'data': [
        'views/account_bank_statement_import_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
