# Copyright 2019 Vicent Cubells - Ingeniería Cloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "fieldservice_logistic_analysis",
    'summary': "",
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Generic',
    'version': '12.0.0.0.1',
    'depends': [
        'fieldservice_logistic',
    ],
    'data': [
        'views/view_analysis.xml',
        'wizards/calcualte_km_wizard_view.xml',
    ],
    'installable': True,
}
