from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

TYPES = [
    ('project', 'Project'),
    ('repair', 'Repair'),
    ('production', 'Production'),
]


class Isets(models.Model):
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
    repair_line_ids = fields.One2many('repair.line', 'iset_id', string='Productos RL')
    stock_move_ids = fields.One2many('stock.move', 'iset_id', string='Productos SM')

    @api.depends('type_id')
    def _set_type(self):
        for record in self:
            record.type = record.type_id.type
    type = fields.Selection(selection=TYPES, string='Type', compute=_set_type)