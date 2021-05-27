from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    name = fields.Char(string='Name')

    udo_template_id = fields.Many2one('udo.template', string='UDO Template')
    udo_qty = fields.Integer(string='Quantity')
    udo_line_ids = fields.One2many('udo.line', 'sale_line_id', string='UDO Line')
    udo_cost_amount = fields.Monetary('UDO Cost')
    udo_sale_amount = fields.Monetary('UDO Sale')

