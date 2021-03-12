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
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'iSets'

    name = fields.Char('Name')
    date = fields.Date('Date')
    start = fields.Float('Start')
    stop = fields.Float('Stop')
    work_id = fields.Many2one('iset.work')
    type = fields.Selection(string='Type', related='work_id.type')
    employee_ids = fields.Many2many('hr.employee')
    repair_id = fields.Many2one('repair.order', string="Repair Order")
    project_id = fields.Many2one('project.project', related='work_id.project_id')
    task_id = fields.Many2one('project.task')
    partner_id = fields.Many2one('res.partner', related='work_id.partner_id')
    workorder_id = fields.Many2one('mrp.workorder')
    mrp_id = fields.Many2one('mrp.production', string='Production')
    repair_service_id = fields.Many2one('product.product', related='work_id.repair_service_id')
    production_loss_id = fields.Many2one('mrp.workcenter.productivity.loss', related='work_id.production_loss_id')
    repair_location_id = fields.Many2one('stock.location', related='repair_id.location_id', string='Origin Location')

    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id
    )
    project_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Proj. Analytic',
        related='project_id.analytic_account_id'
    )
    project_so_id = fields.Many2one('sale.order', related='project_id.sale_order_id', store=True, string='Sale Order')
    mrp_is_locked = fields.Boolean(string='MRP is Locked', related='mrp_id.is_locked')
    mrp_state = fields.Selection(
        string='MRP State', related='mrp_id.state', store=False)
    mrp_date_planned_start = fields.Datetime(
        string='MRP Planned Start',
        store='False',
        related='mrp_id.date_planned_start'
    )
    mrp_date_deadline = fields.Datetime(
        string='MRP deadline',
        store='False',
        related='mrp_id.date_deadline'
    )
    mrp_location_src_id = fields.Many2one('stock.location', string='MRP Location src', store=False, related='mrp_id.location_src_id')
    mrp_location_id = fields.Many2one('stock.location', store=False, related='mrp_id.production_location_id')
    mrp_picking_type_id = fields.Many2one('stock.picking.type', related='mrp_id.picking_type_id', store=False)

    project_service_ids = fields.One2many(
        'account.analytic.line',
        'iset_id',
        domain=[('product_id','=',False),('iset_so_line_id','=',False)],
        store=True,
        string='Imputaciones'
    )
    project_product_ids = fields.One2many(
        'account.analytic.line',
        'iset_id',
        domain=['|',('product_id','!=',False),('iset_so_line_id','!=',False)],
        store=True,
        string='Productos'
    )
    task_sale_order_id = fields.Many2one('sale.order', related='task_id.sale_order_id', string='Sale Order')

    repair_service_ids = fields.One2many('repair.fee', 'iset_id', string='Tech. Services')
    repair_product_ids = fields.One2many('repair.line', 'iset_id', string='Parts')
    mrp_product_ids = fields.One2many('stock.move', 'iset_id', string='Products')
    mrp_service_ids = fields.One2many('mrp.workcenter.productivity', 'iset_id', string='Time consumed')

    loss_id = fields.Many2one('mrp.workcenter.productivity.loss',)

    def create_lot_services_iset(self):
        print("DEBUG")

