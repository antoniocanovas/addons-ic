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

    @api.depends('price_unit', 'product_uom_qty')
    def get_subtotal(self):
        self.subtotal = self.price_unit * self.product_uom_qty

    subtotal = fields.Monetary('Subtotal', currency_field='currency_id', compute="get_subtotal")

    @api.depends('product_id')
    def get_lst_price(self):
        self.lst_price = self.product_id.lst_price

    lst_price = fields.Monetary('List Price', currency_field='currency_id', compute="get_lst_price")

    @api.depends('product_id', 'price_unit')
    def get_lst_price_discount(self):
        if self.price_unit > self.lst_price:
            discount = 0
        else:
            discount = (1 - (self.price_unit / self.lst_price)) * 100
        self.lst_price_discount = discount

    lst_price_discount = fields.Monetary('Discount', currency_field='currency_id',
                                        store=False, compute="get_lst_price_discount")

    @api.depends('product_id')
    def get_price_unit_cost(self):
        self.price_unit_cost = self.product_id.standard_price

    price_unit_cost = fields.Monetary('Cost Price', currency_field='currency_id', compute="get_price_unit_cost")

    @api.depends('product_id')
    def get_price_unit(self):
        self.price_unit = self.product_id.lst_price

    price_unit = fields.Monetary('Price Unit', currency_field='currency_id',  compute="get_price_unit")

