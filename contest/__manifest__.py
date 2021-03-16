{
    'name': "contest",
    'summary': """
        Registrar concursos y ofertas privadas, así como las competencias.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'crm',
    ],
    'data': [
        'views/views.xml',
        'views/view_menu.xml',
        #'views/view_partner_credentials.xml',
        #'security/user_groups.xml',
        'security/ir.model.access.csv',
        #'data/default_rules.xml',
    ],
    'installable': True,
    'application': True,
}
