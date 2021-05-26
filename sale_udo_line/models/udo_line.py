from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoLine(models.Model):
    _name = 'udo.line'
    _description = 'UDO Line'

    name = fields.Char(string='Description')
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity')
    product_uom = fields.Many2one('uom.uom', string='Unit')
    cost_price = fields.Monetary('')
    list_price = fields.Monetary('')
    price_unit = fields.Monetary('')
    discount = fields.Monetary('')
    currency_id = fields.Many2one('res.currency')

    order_line_id = fields.Many2one('sale.order.line', string='Líneas')
