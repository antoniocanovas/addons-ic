{
    'name': 'Product Vehicle',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'fleet_vehicle_category',
        'analytic',
        'sale_management',
        'stock',
        'account',
        'base_automation',
        'product_analytic',
        'crm',
        'crm_product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/action_server.xml',
        'views/model_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
