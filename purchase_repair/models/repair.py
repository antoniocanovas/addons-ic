from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    purchase_order_ids = fields.One2many('purchase.order', 'repair_id')

    def _get_purchase_order_count(self):
        results = self.env['purchase.order'].search([
            ('repair_id', '=', self.id), ]
        )
        self.purchase_order_count = len(results)

    purchase_order_count = fields.Integer('Purchases', compute=_get_purchase_order_count)

    def action_view_purchases(self):
        action = self.env.ref(
            'purchase_repair.action_view_purchases').read()[0]
        return action



