# Copyright 2019 Vicent Cubells - Ingeniería Cloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "fieldservice_logistic",
    'summary': "",
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Generic',
    'version': '12.0.0.0.0',
    'depends': [
        'fleet',
        'fieldservice',
        'fieldservice_isp_flow',
        'fieldservice_fleet',
        'fieldservice_sale',
        'fieldservice_google_map',
    ],
    'data': [
        'views/views_portes.xml',
        'views/views_portes_menu.xml',
    ],
    'installable': True,
}
