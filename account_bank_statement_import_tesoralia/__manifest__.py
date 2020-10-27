# -*- encoding: utf-8 -*-
{
    'name': 'Account Bank Statement Import Tesoralia',
    'category': 'Accounting',
    'version': '12.0.0.0.3',
    'depends': ['account_bank_statement_import','l10n_es_account_bank_statement_import_n43'],
    'description': """ Upload multiple documents n43 formated """,
    'data': [
        'views/account_menu_config_n43_massive_import.xml',
        'views/res_company_views.xml',
        'security/ir.model.access.csv',
        'data/automatic_n43_import.xml',
    ],
    'installable': True,
}
