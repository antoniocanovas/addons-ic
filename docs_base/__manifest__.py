{
    'name': 'Docs Base',
    'version': '12.0.1.0',
    'category': 'Documentation',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/docs_report.xml',
        'data/mail_template_data.xml',
        'views/views.xml',
        'views/views_menu.xml',
    ],
    'installable': True,
}
