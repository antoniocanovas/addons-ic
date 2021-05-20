{
    'name': 'iSet Timesheet',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'isets',
        'base_automation',


    ],
    'data': [
        #'views/menu_views.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/model_views.xml',
        'data/automatic_actions.xml',
    ],
    'installable': True,
}
