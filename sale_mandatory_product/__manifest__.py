{
    'name': 'Sale Mandatory Product',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'base_automation',
    ],
    'data': [
        'data/server_action.xml',
        'views/sale_order_views.xml',
        'views/product_views.xml',
        #'data/data.xml',
    ],
    'installable': True,
}
