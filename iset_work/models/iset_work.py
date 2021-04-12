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
    note = fields.Text('Note')
    protection_product_ids = fields.Many2many('product.product', string='Protection')
    location_id = fields.Many2one('stock.location', string='Location')
    quant_ids = fields.Many2many('stock.quant', string='Stock')
    #tool_product_ids = fields.Many2many('product.product', string='Tools')

    def _get_sale_order_count(self):
        self.sale_order_count = len(self.sale_order_ids)

    sale_order_count = fields.Integer('Attachments', compute=_get_sale_order_count, store=False)

    def _get_projects_count(self):
        self.projects_count = len(self.project_ids)

    projects_count = fields.Integer('Attachments', compute=_get_projects_count, store=False)

