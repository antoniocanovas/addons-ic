{
    'name': "odoo sso server",
    'summary': """
        Amplia la vista credentials para conexión sso a otras instancias de Odoo.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '13.0.1.0.0',
    'depends': [
        'odoo_sso_client',
        'partner_credentials',
    ],
    'data': [
        'views/view.xml',
        'data/user_data.xml',
    ],
    'installable': True,
    'application': True,
}
