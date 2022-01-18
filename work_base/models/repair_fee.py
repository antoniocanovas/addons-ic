from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairFee(models.Model):
    _inherit = 'repair.fee'

    work_base_id = fields.Many2one('work.base')
    type_id = fields.Many2one('working.type', 'Type')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    date = fields.Date(string='Date')
