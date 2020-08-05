{
    'name': "Caritas",
    'summary': """
        Descripción : ""
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.0.0.2',
    'depends': [
        'contacts',
        'sale',
    ],
    'data': [
        'views/res_company_caritas.xml',
        'views/res_partner_caritas.xml',
        'views/res_config_settings_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
