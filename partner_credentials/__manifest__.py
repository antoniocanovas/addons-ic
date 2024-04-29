{
    'name': "partner credentials",
    'summary': """
        Añade un nuevo modelo para documentar usuario y contraseña de aplicaciones, y añade
        al usuario un botón para ver los accesos configurados para este.
        Faltan las reglas de acceso.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'contacts',
        'hr',
    ],
    'data': [
        'views/views.xml',
        'views/view_menu.xml',
        'views/view_partner_credentials.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/default_rules.xml',
    ],
    'installable': True,
    'application': True,
}
