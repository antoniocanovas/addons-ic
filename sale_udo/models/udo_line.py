from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoLine(models.Model):
    _name = 'udo.line'
    _description = 'UDO Line'


    product_id = fields.Many2one('product.product', string='Product')

    product_uom_qty = fields.Float(string='Quantity')
    product_uom = fields.Many2one('uom.uom', string='Unit', related='product_id.uom_id')
    currency_id = fields.Many2one('res.currency')
    discount = fields.Monetary('Discount', currency_field='currency_id')
    sale_line_id = fields.Many2one('sale.order.line', string='Líneas')
    name = fields.Char(string='Description')
    price_unit_cost = fields.Monetary('Cost Price', currency_field='currency_id')
    list_price = fields.Monetary('Price', currency_field='currency_id')
    price_unit = fields.Monetary('Price Unit', currency_field='currency_id')

    @api.depends('price_unit', 'product_uom_qty')
    def get_subtotal(self):
        self.subtotal = self.price_unit * self.product_uom_qty

    subtotal = fields.Monetary('Subtotal', currency_field='currency_id', compute="get_subtotal")
