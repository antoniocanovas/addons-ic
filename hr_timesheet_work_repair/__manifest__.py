{
    'name': 'Timesheet Work Repair',
    'version': '14.0.7.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'hr_timesheet_work_extended',
        'repair',
    ],
    'data': [
        'views/model_views.xml',
        'views/menu_views.xml',
        'views/templates.xml',
        'views/view_repair_order_timesheets.xml',
    ],
    'installable': True,
}