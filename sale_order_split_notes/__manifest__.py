# -*- coding: utf-8 -*-
{
    'name': "sale_order_split_notes",

    'summary': """
        Cut lines in order notes in a budget.""",

    'description': """
        Cut the order notes in a budget, so as not to leave blank spaces when printing a budget
        with many notes.
    """,

    'author': "ic",
    'website': "http://www.ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
               'mail',
               'sale',],

    # always loaded
    'data': [
        'views/views.xml',
        'data/server_action.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
