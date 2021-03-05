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
    type_id = fields.Many2one('iset.types')
    type = fields.Selection(selection=TYPES, string='Type', related='type_id.type')
    employee_ids = fields.Many2many('hr.employee')
    repair_id = fields.Many2one('repair.order', string="Reparación")
    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task')
    workorder_id = fields.Many2one('mrp.workorder')

    repair_location_id = fields.Many2one('repair.order', related='repair_id.location_id', string='R.Localización')

    project_service_ids = fields.One2many(
        'account.analytic.line',
        'iset_id',
        domain="[('product_id.type','=','service')]",
        string='Imputaciones'
    )
    project_product_ids = fields.One2many(
        'account.analytic.line',
        'iset_id',
        domain="[('product_id.type','!=','service')]",
        string='Productos'
    )
    task_sale_order_id = fields.Many2one('sale.order',related='task_id.sale_order_id', string='Venta')

    mrp_id = fields.Many2one('mrp.production', string='Mrp')


    repair_product_ids = fields.One2many('repair.fee', 'iset_id', string='Horas asistencias')
    repair_service_ids = fields.One2many('repair.line', 'iset_id', string='Productos RL')
    mrp_product_ids = fields.One2many('stock.move', 'iset_id', string='Productos SM')
    mrp_service_ids = fields.One2many('mrp.workcenter.productivity', 'iset_id', string='Partes producción')
