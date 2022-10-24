# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

class PurchaseOrderLinePriceHistoryLine(models.TransientModel):
    _inherit = "purchase.order.line.price.history.line"

    discount = fields.Float(
        string='Discount',
        related='purchase_order_line_id.discount'
    )

    @api.depends('price_unit', 'discount')
    def get_purchase_net_price(self):
        self.ensure_one()
        for record in self:
            record.price_net = record.price_unit * (1 - record.discount/100)
    price_net = fields.Float(
        string='Net price',
        store=False,
        compute='get_purchase_net_price',
    )
