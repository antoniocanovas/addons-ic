{
    'name': 'iSets',
    'version': '14.0.6.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_timesheet',
        #'hr_timesheet',
        'repair',
        'mrp',

    ],
    'data': [
        'security/ir.model.access.csv',
        'data/action_server.xml',
        'data/data.xml',
        'data/rules.xml',
        'views/model_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
