# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProjectRoadmap(models.Model):
    _name = 'project.roadmap'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project roadmap'

    name = fields.Char(string='Name', required=True, copy=True, tracking=True)
    display_name = fields.Char(string='Display name', store=False, compute="_name_get")
    sequence = fields.Integer(string='Sequence', default="1", copy=True)
    is_favorite = fields.Boolean('Is favorite', copy=False)
    user_id = fields.Many2one('res.users', string='User', required=True, store=True, copy=True, tracking=True)
    date_limit = fields.Date(string='Date limit', copy=False, tracking=True)
    project_id = fields.Many2one('project.project', string='Project', copy=True)
    manager_id = fields.Many2one('res.users', related='project_id.user_id', store=True, string='Project manager')
    partner_id = fields.Many2one(related='project_id.partner_id', string="Customer", copy=True, tracking=True)
    contact_id = fields.Many2one('res.partner', string="Contact", copy=True, tracking=True)
    type = fields.Selection([('lead','Lead'), ('sale','Sale'), ('purchase','Purchase'), ('task','Task'),
                             ('project','Project'),('picking','Picking'),('invoice','Invoice')], required=True)
    roadmap_user_avatar = fields.Binary(string="Avatar", related="user_id.partner_id.image_128")
    lead_id = fields.Many2one('crm.lead', string='Lead')
    sale_id = fields.Many2one('sale.order', string='Sale order')
    purchase_id = fields.Many2one('purchase.order', string='Purchase order')
    task_id = fields.Many2one('project.task', string='Task')
    picking_id = fields.Many2one('stock.picking', string='Picking')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    active = fields.Boolean('Active', default=True, copy=False, tracking=True)

    @api.depends('lead_id.probability', 'sale_id.state', 'purchase_id.state', 'task_id.stage_id', 'picking_id.state',
                 'invoice_id.state')
    def _name_get(self):
        for record in self:
            name = "[" + str(record.sequence) + "] " + record.type +  ": " + " " + record.name
            record['display_name'] = name

    @api.depends('lead_id.stage_id', 'sale_id.state', 'purchase_id.state', 'task_id.stage_id', 'picking_id.state',
                 'invoice_id.state', 'invoice_id.payment_state','project_id.task_ids.stage_id')
    def _get_roadmap_state(self):
        for record in self:
            state = 'New'
            if (record.type == 'lead') and (record.lead_id.id):
                state = record.lead_id.stage_id.name
            elif (record.type == 'sale') and (record.sale_id.id):
                state = record.sale_id.state
            elif (record.type == 'purchase') and (record.purchase_id.id):
                state = record.purchase_id.state
            elif (record.type == 'task') and (record.task_id.id):
                state = record.task_id.stage_id.name
            elif (record.type == 'project') and (record.project_id.id):
                state = "Finalizado"
                if record.project_id.task_ids.ids:
                    tasks = record.env['project.task'].search([('project_id','=',record.project_id.id), ('is_closed','!=',True)])
                    recs_sorted = tasks.sorted(key=lambda r: r.stage_id.sequence)
                    if tasks.ids:
                        state = recs_sorted[0].stage_id.name
            elif (record.type == 'picking') and (record.picking_id.id):
                state = record.picking_id.state
            elif (record.type == 'invoice') and (record.invoice_id.id) and (record.invoice_id.state != 'posted'):
                state = record.invoice_id.state
            elif (record.type == 'invoice') and (record.invoice_id.id) and (record.invoice_id.state == 'posted'):
                state = record.invoice_id.payment_state
            record.state = state
    state = fields.Char(string='State', compute="_get_roadmap_state", store=True, default='New')
