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

    @api.depends('product_id')
    def get_product_name(self):
        for record in self:
            record.name = record.product_id.name

    name = fields.Char(string='Description', compute='get_product_name')

    @api.depends('product_id')
    def get_product_price(self):
        for record in self:
            record.cost_price = record.product_id.standard_price

    cost_price = fields.Monetary('Cost Price', currency_field='currency_id', compute='get_product_price')

    @api.depends('product_id')
    def get_product_list_price(self):
        for record in self:
            record.list_price = record.product_id.list_price
    list_price = fields.Monetary('Price', currency_field='currency_id', compute='get_product_list_price')

    @api.depends('product_id')
    def get_product_unit_price(self):
        for record in self:
            record.price_unit = record.product_id.list_price
    price_unit = fields.Monetary('Price Unit', currency_field='currency_id',  compute='get_product_list_price')