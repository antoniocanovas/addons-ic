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
    ],
    'data': [
        #'security/ir.model.access.csv',
        'data/action_server.xml',
        #'data/data.xml',
        #'data/rules.xml',
       # 'views/model_views.xml',
        'views/menu_views.xml',
        #'views/templates.xml',
        #'views/iset_report.xml',
    ],
    'installable': True,
}
