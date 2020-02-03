{
    'name': 'Docs',
    'version': '12.0.4.0',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'expedients',
        'project_task_contacts',
        'project_task_project_contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/docs_report.xml',
        'data/mail_template_data.xml',
        'views/views.xml',
        'views/views_menu.xml',
    ],
    'installable':True,
}
