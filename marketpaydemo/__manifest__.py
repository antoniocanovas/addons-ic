# -*- coding: utf-8 -*-

{
    'name': "marketpaydemo",

    'summary': """
        Modulos marketpay""",

    'description': """
        develop
    """,

    'author': "Pedro Guirao",
    'website': "https://ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','payment','website_sale',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/partner_marketpay_view.xml',
        'views/acquirer_marketpay_view.xml',
        'views/payment_marketpay_templates.xml',
        'data/payment_marketpay.xml'
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
