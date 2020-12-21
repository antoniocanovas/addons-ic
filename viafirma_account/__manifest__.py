# -*- coding: utf-8 -*-
{
    'name': "viafirma facturas",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ic",
    'website': "http://www.ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.0.2.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account',
               'viafirma'],

    # always loaded
    'data': [
        'views/viafirma_account_invoice_report.xml',
        'views/views_account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
