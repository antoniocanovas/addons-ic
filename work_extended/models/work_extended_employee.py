from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class iSetWorkEmployee(models.Model):
    _name = 'work.extended.employee'
    _description = 'iSetWorkEmployee'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    work_extended_id = fields.Many2one('work.extended', 'Work Extended')
    function_ids = fields.Many2many('hr.job')

