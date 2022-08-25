{
    'name': 'Project Roadmap',
    'version': '14.0.0.1',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'crm',
        'project',
        'sale_management',
        'purchase',
        'stock',
        'account',
        'base_automation',
        'web_widget_open_tab',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/project_roadmap_view.xml',
        'views/project_view.xml',
        'views/project_task_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/stock_picking_view.xml',
        'views/account_move_view.xml',
        'views/crm_lead_view.xml',
        'views/views_menu.xml',
    ],
    'installable':True,
}
