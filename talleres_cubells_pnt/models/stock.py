# -*- coding: utf-8 -*-
from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    supplier_picking = fields.Char('Supplier picking')
    partner_shipping_delivery_id = fields.Many2one('res.partner',
                                                   'Delivery address')

    #@api.model
    #def create(self, values):
    #    res = super(StockPicking, self).create(values)
    #    if res.origin:
    #        sale_id = self.env['sale.order'].search(
    #            [('name', '=', res.origin)])
    #        if len(sale_id) == 1:
    #            res.partner_id = sale_id.partner_id
    #            if not res.partner_shipping_delivery_id:
    #                res.partner_shipping_delivery_id = \
    #                    sale_id.partner_shipping_id
    #    return res
