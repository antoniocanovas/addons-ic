{
    'name': "partner credential",
    'summary': """
        Nuevo modelo para documentar usuario y contraseña de aplicaciones.
        """,
    'author': "Antonio Cánovas",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '16.0.2.0.0',
    'depends': [
        'web',
        'contacts',
        'hr',
        'field_encryption',
    ],
    'external_dependencies': {"python": ["pyotp", "cryptography"]},
    'data': [
        'security/user_groups.xml',
        'views/partner_credential_views.xml',
        'views/partner_credential_category_views.xml',
        'views/menu_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'data/default_rules.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'partner_credential/static/src/js/copy_clipboard.js',
        'partner_credential/static/src/xml/copy_clipboard.xml',
    ],
},
    'installable': True,
    'application': True,
}
