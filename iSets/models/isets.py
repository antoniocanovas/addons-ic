from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class iSets(models.Model):
    _name = 'isets'
    _description = 'iSets'

    name = fields.Char('Name')
    date = fields.Date('Date')
    start = fields.Float('Start')
    end = fields.Float('End')
    type_id = fields.Many2one('iset_types')
    employee_ids = fields.Many2many('hr.employee')
    repair_id = fields.Many2one('repair.order')
    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task')
    workorder_id = fields.Many2one('mrp.workorder')

    timesheet_ids = fields.One2many('account.analytic.line', 'iset_id', string='Imputaciones')
    productivity_ids = fields.One2many('mrp.workcenter.productivity', 'iset_id', string='Partes producción')
    repair_fee_ids = fields.One2many('repair.fee', 'iset_id', string='Horas asistencias')