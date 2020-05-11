{
    'name': 'Docs',
    'version': '12.0.5.0',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'project_task_contacts',
        'project_task_project_contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/docs_report.xml',
        'data/mail_template_data.xml',
        'data/ir_rule.xml',
        'views/views.xml',
        'views/views_menu.xml',
        'views/docs_portal.xml',
    ],
    'installable': True,
}
