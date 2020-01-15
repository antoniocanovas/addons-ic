# Copyright 2019 Vicent Cubells - Ingeniería Cloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Sale Timesheet Logistic",
    'summary': "",
    'author': "Cubells",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Generic',
    'version': '13.0.4.0.2',
    'depends': [
        'fleet',
        'industry_fsm',
        'sale_timesheet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/project_task_views.xml',
        'views/project_task_form_fsm_views.xml',
        'views/fleet_vehicle_views.xml',
    ],
    'installable': True,
}
