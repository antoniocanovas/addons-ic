# -*- coding: utf-8 -*-
{
    'name': "viafirma documents",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Pedro Baños",
    'website': "http://www.ingenieriacloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Digital Signature',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['documents_dms',
               'viafirma'],

    # always loaded
    'data': [
        'data/viafirma_document_context_action.xml',
        'views/document_viafirma_document.xml',
        'views/res_company_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
