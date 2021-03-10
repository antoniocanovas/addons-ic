{
    'name': 'iSets',
    'version': '14.0.3.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'hr_timesheet',
        'repair',
        'mrp',

    ],
    'data': [
        'views/menu_views.xml',
        'security/ir.model.access.csv',
        'views/model_views.xml',
        'data/action_server.xml',
    ],
    'installable': True,
}
