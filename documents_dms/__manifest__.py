# -*- coding: utf-8 -*-
{
    'name': "Documents DMS",

    'summary': """
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Pedro Guirao",
    'website': "http://www.ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'documents',
            ],

    # always loaded
    'data': [
        'views/document_dms.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
