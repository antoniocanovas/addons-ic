# -*- coding: utf-8 -*-

{
    'name': 'Project Checklist',
    'version': '16.0.1.0.0',
    'category': 'Project/Project',
    'summary': "To Manage the Project's and task's checklists",
    'description': "To Manage the Project's and task's checklists",
    'author': 'Serincloud',
    'company': 'Serincloud',
    'maintainer': 'Serincloud',
    'website': 'https://www.ingenieriacloud.com',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_checklist_views.xml',
        'views/project_task_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {},

    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
