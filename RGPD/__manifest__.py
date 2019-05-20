# -*- coding: utf-8 -*-

{
    'name': "RGPD",

    'summary': """
        Modulos RGPD """,

    'description': """
       *****
    """,

    'author': "Pedro Guirao",
    'website': "https://ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [

        'views/views.xml',
        #'views/medidas_view.xml',
        'demo/demo.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
