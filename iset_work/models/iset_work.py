from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class iSetsWork(models.Model):
    _name = 'iset.work'
    _inherit = ['iset.work','mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users', string='Supervisor')
    saleperson_id = fields.Many2one('res.users', string='Salesman')
    sale_order_ids = fields.One2many('sale.order', 'iset_work_id')
    project_ids = fields.One2many('project.project', 'iset_work_id')
    employee_line_ids = fields.One2many('iset.work.employee', 'iset_work_id', string="Employees")
    note = fields.Text('Note')
    protection_product_ids = fields.Many2many('product.product', string='Protection')
    location_id = fields.Many2one('stock.location', string='Location')

    tool_product_ids = fields.Many2many('product.product', 'rel_product_iset_work', 'iset_work_id', 'product_id', string='Tools')

    def _get_sale_order_count(self):
        self.sale_order_count = len(self.sale_order_ids)

    sale_order_count = fields.Integer('Attachments', compute=_get_sale_order_count, store=False)

    def _get_projects_count(self):
        self.projects_count = len(self.project_ids)

    projects_count = fields.Integer('Attachments', compute=_get_projects_count, store=False)

    @api.depends('create_date')
    def _get_quant_ids(self):
        for record in self:
            quants = self.env['stock.quant'].search([('quantity','>', 0), ('location_id', '=', record.location_id.id)]).ids
            record['quant_ids'] = [(6, 0, quants)]

    quant_ids = fields.Many2many('stock.quant', string='Stock', compute=_get_quant_ids)

