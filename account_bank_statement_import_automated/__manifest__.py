# -*- encoding: utf-8 -*-
{
    'name': 'Account Bank Statement Import Automated',
    'category': 'Accounting',
    'version': '12.0.0.0.1',
    'depends': ['account_bank_statement_import','l10n_es_account_bank_statement_import_n43'],
    'description': """ Upload multiple documents n43 formated """,
    'data': [
        'views/account_bank_statement_import_view.xml',
        'views/account_menu_config_n43_massive_import.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
