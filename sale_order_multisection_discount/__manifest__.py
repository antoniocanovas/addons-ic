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
        #'data/crea_lineas_factura.xml',
        'data/server_actions.xml',
        'views/sale_order_wizard_multisection_discount.xml',
        'views/sale_order_views.xml',
        'security/ir.model.access.csv',
        #'data/automatic_actions.xml',
        #'views/report_sale_order.xml',
        #'views/account_report.xml',
    ],
    'installable': True,
}
