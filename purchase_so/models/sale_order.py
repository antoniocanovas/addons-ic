from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_ids = fields.One2many('purchase.order', 'sale_id')

    def _get_purchase_order_count(self):
        results = self.env['purchase.order'].search([
            ('sale_id', '=', self.id), ]
        )
        self.purchase_order_count = len(results)

    purchase_order_count = fields.Integer('Purchases', compute=_get_purchase_order_count)

    def action_view_purchases(self):
        action = self.env.ref(
            'purchase_so.action_view_purchases_so').read()[0]
        return action



