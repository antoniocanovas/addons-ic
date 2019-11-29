{
    'name': "user manager permision limit",
    'summary': """
       Plantilla por defecto para nuevas Empresas en multiempresa, se aplica al crear.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '12.0.3.0.0',
    'depends': [

    ],
    'data': [
        #'data/default_rules.xml',
        #'data/default_actions.xml',
        #'views/view.xml',
        'views/res_user_groups.xml',
        'security/user_groups.xml',
        #'security/ir.model.access.csv',
        #'data/default_data.xml',

    ],
    'installable': True,
    'application': True,
}
