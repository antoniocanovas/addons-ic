{
    'name': "odoo sso client",
    'summary': """
       Añade el usuario requerido para conectar desde un Odoo maestro a esta instancia. 
       No afecta al entorno de usuario, crea un usuario interno.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.7.0.0',
    'depends': [
    ],
    'data': [
        #'security/user_groups.xml',
        #'security/ir.model.access.csv',
        'data/user_data.xml',
    ],
    'installable': True,
    'application': True,
}
