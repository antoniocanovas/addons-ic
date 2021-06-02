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
    sale_line_id = fields.Many2one('sale.order.line', string='Líneas')
    name = fields.Char(string='Description')
    sale_id = fields.Many2one('sale.order', related='sale_line_id.order_id', string='Sale')

    @api.depends('price_unit', 'product_uom_qty')
    def get_subtotal(self):
        for record in self:
            record.subtotal = record.price_unit * record.product_uom_qty

    subtotal = fields.Monetary('Subtotal', currency_field='currency_id', compute="get_subtotal")

    @api.depends('product_id')
    def get_lst_price(self):
        for record in self:
            record.lst_price = record.product_id.lst_price

    lst_price = fields.Monetary('List Price', currency_field='currency_id', compute="get_lst_price")

    @api.depends('product_id', 'price_unit')
    def get_lst_price_discount(self):
        for record in self:
            if record.lst_price > 0:
                if record.price_unit > record.lst_price:
                    discount = 0
                else:
                    discount = (1 - (record.price_unit / record.lst_price)) * 100
                record.lst_price_discount = discount

    lst_price_discount = fields.Monetary('Discount', currency_field='currency_id',
                                        store=False, compute="get_lst_price_discount")

    @api.depends('product_id')
    def get_price_unit_cost(self):
        for record in self:
            record.price_unit_cost = record.product_id.standard_price

    price_unit_cost = fields.Monetary('Cost Price', currency_field='currency_id',
                                      readonly=False, store=True, compute="get_price_unit_cost")

    @api.depends('product_id')
    def get_price_unit(self):
        for record in self:
            record.price_unit = record.product_id.lst_price

    price_unit = fields.Monetary('Price Unit', currency_field='currency_id',
                                 store=True, readonly=False, compute="get_price_unit")

