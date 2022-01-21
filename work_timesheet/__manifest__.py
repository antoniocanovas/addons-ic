{
    'name': 'Work Base Timesheet',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'work_base',
        'base_automation',


    ],
    'data': [
        'security/ir.model.access.csv',

        'views/model_views.xml',
        'views/menu_views.xml',
        'data/automatic_actions.xml',
        'data/rules.xml',
    ],
    'installable': True,
}
