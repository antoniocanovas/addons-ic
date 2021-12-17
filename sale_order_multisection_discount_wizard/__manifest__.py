{
    'name': 'Sale Order Multisection Discount',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_order_multisection',
    ],
    'data': [
        'data/server_actions.xml',
        'views/sale_order_wizard_multisection_discount.xml',
        'views/sale_order_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
