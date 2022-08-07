{
    'name': "contest",
    'summary': """
        Registrar concursos y ofertas privadas, así como las competencias.
        """,
    'author': "Serincloud SL",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'crm',
    ],
    'data': [
        'views/views.xml',
        'views/views_crm.xml',
        'views/views_res_partner.xml',
        'views/view_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
