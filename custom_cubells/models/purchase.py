# -*- coding: utf-8 -*-
from odoo import models, api, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    wo_num = fields.Char('WO Num')

    #@api.onchange('product_id')
    #def onchange_product_id(self):
    #    res = super(PurchaseOrderLine, self).onchange_product_id()

    #    if self.product_id.product_tmpl_id.id and self.partner_id.id:
    #        product_name_seller = self.env["product.supplierinfo"].search([
    #            ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id),
    #            ('name', '=', self.partner_id.id)
    #        ])

    #        for product in product_name_seller:
    #            if product_name_seller:
    #                self.name = product.product_name
    #    return res


class StockMove(models.Model):
    _inherit='stock.move'

    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        related="purchase_line_id.order_id.partner_id",
        store=True
    )
    supplier_reference = fields.Char(
        string='Reference',
        related="purchase_line_id.order_id.partner_ref",
        readonly=True,
    )
    description_purchase_line = fields.Text(
        string='Description',
        related="purchase_line_id.name",
        readonly=True,
    )
    wo_num = fields.Char(
        string='Nº OT',
        related="purchase_line_id.wo_num",
        store=True
    )
    quantity = fields.Float(
        string='Quantity',
        related="purchase_line_id.product_qty",
        readonly=True,
    )
    date_price = fields.Date(
        string='Date Price'
    )
    price_unit = fields.Float(
        string='Price Unit',
        related="purchase_line_id.price_unit",
        readonly=True,
    )
    discount = fields.Float(
        string='Discount',
        related="purchase_line_id.discount",
        readonly=True,
    )
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal_line'
    )

    #def _compute_subtotal_line(self):
    #    for record in self:
    #        for order in record.purchase_line_id:
    #            record.date_price = order.date_price
    #            record.subtotal = order.price_subtotal
