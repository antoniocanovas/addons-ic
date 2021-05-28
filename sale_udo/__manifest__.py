{
    'name': 'UDO',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'product_brand',
        'hr',


    ],
    'data': [

        'security/ir.model.access.csv',
        'views/model_views.xml',
        'views/menu_views.xml',
        'views/sale_order_views.xml',
        'data/server_action.xml',
        #'data/data.xml',
    ],
    'installable': True,
}
