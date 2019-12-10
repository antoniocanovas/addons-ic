{
    'name': 'Case Docs',
    'version': '12.0.0.1',
    'category': 'Projects',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
       'expedientes',
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
        #'views/project_view.xml',
        #'data/actions.xml'
        #'data/ir_ui_menu.xml',
    ],
    'installable':True,
}
