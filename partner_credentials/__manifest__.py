{
    'name': "partner credentials",
    'summary': """
       Añade la funcionalidad de conectarse a un odoo cliente con un usuario preasignado.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.1.0.0',
    'depends': [
        'contacts',
    ],
    'data': [
        'views/views.xml',
        'views/view_menu.xml',
        'views/view_partner_credentials.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
