{
    'name': 'Expedientes',
    'version': '12.0.2.0',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'project',
        'project_stage_closed',
        'project_task_dependency',
        'project_task_default_stage',
        'hr',
        'base_automation',
    ],
    'data': [
        #'data/ir_model_fields.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'data/actions.xml'
        #'data/ir_ui_menu.xml',
    ],
    'installable':True,
}
