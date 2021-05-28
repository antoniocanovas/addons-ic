from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name = fields.Char(string='Name')
    udo_template_id = fields.Many2one('udo.template', string='UDO Template')
    udo_line_ids = fields.One2many('udo.line', 'sale_line_id', string='UDO Line')

    def get_udo_cost_amount(self):
        cost = 0
        for line in self.udo_line_ids:
            cost += line.price_unit_cost * line.product_uom_qty
        self.udo_cost_amount = cost

    udo_cost_amount = fields.Monetary('UDO Cost', store=False, compute='get_udo_cost_amount')


