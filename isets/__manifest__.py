{
    'name': 'iSets',
    'version': '14.0.6.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale',
        'project',
        'hr_timesheet',
        'repair',
        'mrp',

    ],
    'data': [

        'security/ir.model.access.csv',
        'views/model_views.xml',
        'views/menu_views.xml',
        'data/action_server.xml',
        'data/data.xml',
    ],
    'installable': True,
}
