{
    'name': 'Timesheet Work Section to Timesheet Done',
    'version': '14.0.1.0.0',
    'category': '',
    'description': u"""
Add sale line section in timesheet.work.done to allow filtering and grouping by.
""",
    'author': 'Serincloud',
    'depends': [
        'sale_order_multisection',
        'hr_timesheet_work',
    ],
    'data': [
        'views/timesheet_line_todo_views.xml',
        'views/timesheet_line_done_views.xml',
    ],
    'installable': True,
}
