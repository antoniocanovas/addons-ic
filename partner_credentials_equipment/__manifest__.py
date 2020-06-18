{
    'name': "partner credentials Equipment",
    'summary': """
        Añade un nuevo menú para añadir dispositivos y vincularlos a las credenciales creadas.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.1.0.1',
    'depends': [
        'partner_credentials',
        'maintenance',
    ],
    'data': [
        'views/views.xml',
        #'views/view_menu.xml',
        #'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
