{
    'name': 'Purchase SO',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'base_automation',
        'purchase',
        'sale',

    ],
    'data': [
        'views/purchase_so_views.xml',
        'data/server_action.xml',
    ],
    'installable': True,
}
