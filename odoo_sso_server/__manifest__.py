{
    'name': "odoo sso server",
    'summary': """
       Añade la funcionalidad de conectarse a un odoo cliente con un usuario preasignado.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.5.0.0',
    'depends': [
        'odoo_sso_client',
    ],
    'data': [
        'views/view.xml',
    ],
    'installable': True,
    'application': True,
}
