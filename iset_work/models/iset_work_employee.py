from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class iSetWorkEmployee(models.Model):
    _name = 'iset.work.employee'
    _description = 'iSetWorkEmployee'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    iset_work_id = fields.Many2one('iset.work', 'iSet Work')
    function_ids = fields.Many2many('hr.job')

