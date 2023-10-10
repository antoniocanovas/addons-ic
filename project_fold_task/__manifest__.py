# -*- coding: utf-8 -*-

{
    'name': 'Project fold in tasks',
    'version': '16.0.1.0.0',
    'category': 'Project/Project',
    'summary': "Project fold boolean field in tasks",
    'description': "Related field from project in task to hide them if project stage is folded (useful for templates, finnished an cancelled",
    'author': 'Serincloud',
    'company': 'Serincloud',
    'maintainer': 'Serincloud',
    'website': 'https://www.ingenieriacloud.com',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_task_views.xml',
    ],
    'assets': {},

    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
