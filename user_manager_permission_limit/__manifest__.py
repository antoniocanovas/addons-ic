{
    'name': "user manager permision limit",
    'summary': """
        Oculta la opción de permisos de Administración para el grupo user manager, solo tendrán acceso aquellos
        usuarios con "base.group_system".
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_user_groups.xml',
    ],
    'installable': True,
    'application': True,
}
