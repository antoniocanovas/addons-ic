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
    'version': '12.0.4.0.0',
    'depends': [

    ],
    'data': [
        'views/res_user_groups.xml',
        #'security/menu_access.xml',
    ],
    'installable': True,
    'application': True,
}
