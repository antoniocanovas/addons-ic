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

    name = fields.Char('Name', required=True)
    date = fields.Date('Date')
    start = fields.Float('Start')
    stop = fields.Float('Stop')
    work_id = fields.Many2one('iset.work')
    type = fields.Selection(string='Type', related='work_id.type')
    employee_ids = fields.Many2many('hr.employee')
    repair_id = fields.Many2one('repair.order', string="Repair Order")
    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task')
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

    @api.onchange('work_id')
    def get_productions(self):
        for record in self:
            partner = record.work_id.partner_id
            sale = record.work_id.production_sale_id
            productions = []
            if (partner.id) and (not sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([('partner_id', '=', partner.id)]).ids
            elif (not partner.id) and (sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([('sale_id', '=', sale.id)]).ids
            elif (partner.id) and (sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([('sale_id', '=', sale.id)]).ids
            elif (not partner.id) and not (sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([]).ids
            record.production_ids = [(6, 0, productions)]

    production_ids = fields.Many2many('mrp.production', compute=get_productions, store=False)

    @api.onchange('work_id')
    def get_repairs(self):
        for record in self:
            repairs = []
            partner = record.work_id.partner_id
            if (partner.id) and (record.type == 'repair'):
                repairs = self.env['repair.order'].search([('partner_id', '=', partner.id)]).ids
            elif (not partner.id) and (record.type == 'repair'):
                repairs = self.env['repair.order'].search([]).ids
            record.repair_ids = [(6, 0, repairs)]

    repair_ids = fields.Many2many('repair.order', compute=get_repairs, store=False)

    @api.onchange('work_id')
    def get_projects(self):
        for record in self:
            for record in self:
                projects = []
                partner = record.work_id.partner_id
                project = record.work_id.project_id
                if (partner.id) and (not project.id) and (record.type == 'project'):
                    projects = self.env['project.project'].search([('partner_id', '=', partner.id)]).ids
                elif (not partner.id) and (project.id) and (record.type == 'project'):
                    projects = self.env['project.project'].search([('id', '=', project.id)]).ids
                elif (partner.id) and (project.id) and (record.type == 'project'):
                    projects = self.env['project.project'].search([('id', '=', project.id)]).ids
                elif (not partner.id) and not (project.id) and (record.type == 'project'):
                    projects = self.env['project.project'].search([]).ids
                record.project_ids = [(6, 0, projects)]

    project_ids = fields.Many2many('project.project', compute=get_projects, store=False)

    @api.onchange('work_id', 'workorder_id')
    def get_allow_services(self):
        for record in self:
            allow = False
            if (record.type == 'project') and (record.project_id.id != False): allow = True
            if (record.type == 'production') and (record.workorder_id.id != False): allow = True
            if (record.type == 'repair') and (record.repair_id.id != False): allow = True
            record.allow_services = allow

    allow_services = fields.Boolean(store=True, compute=get_allow_services)

    @api.onchange('work_id')
    def get_production_loss(self):
        for record in self:
            record.production_loss_id = record.work_id.production_loss_id.id

    production_loss_id = fields.Many2one('mrp.workcenter.productivity.loss', string='Loss', readonly=False,
                                         compute=get_production_loss)

    def create_lot_services_iset(self):
        print("DEBUG")

