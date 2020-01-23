# Copyright 2020 Ingeniería Cloud - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Retenciones IRNR (No residentes) para contactos",
    'version': '12.0.1.0.0',
    'category': 'Localization',
    'depends': [
        'l10n_es_aeat',
        'l10n_es_irnr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/nrc.xml',
        'views/nrc_views.xml',
        'views/res_partner_views.xml',
        'wizards/create_nrc_file_views.xml',
    ],
    'author': 'cubells',
    'website': 'https://ingenieriacloud.com',
    'license': 'AGPL-3',
    'installable': True,
}
