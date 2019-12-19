{
    'name': "odoo sso client",
    'summary': """
       Añade la funcionalidad de conectarse a este odoo cliente con un usuario preasignado.
       Para el servidor es necesario instalar odoo sso server.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.5.0.0',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'data/user_data.xml',
    ],
    'installable': True,
    'application': True,
}
