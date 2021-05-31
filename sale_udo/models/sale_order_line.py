from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name = fields.Char(string='Name')
    udo_template_id = fields.Many2one('udo.template', string='UDO Template')
    udo_line_ids = fields.One2many('udo.line', 'sale_line_id', string='UDO Line')

    def get_udo_cost_amount(self):
        for record in self:
            cost = 0
            for line in record.udo_line_ids:
                cost += line.price_unit_cost * line.product_uom_qty
            record.udo_cost_amount = cost

    udo_cost_amount = fields.Monetary('UDO Cost', store=False, compute='get_udo_cost_amount')

    @api.depends('product_id')
    def get_lst_price(self):
        for record in self:
            record.lst_price = record.product_id.lst_price

    lst_price = fields.Monetary('List Price', currency_field='currency_id', compute="get_lst_price")

    @api.depends('product_uom', 'price_unit')
    def get_lst_price_discount(self):
        for record in self:
            discount, qty_uom = 0, 0
            lst_price = record.product_id.lst_price

            if record.product_id.id and (record.product_uom_qty > 0):
                if record.product_uom.uom_type == 'reference':
                    qty_uom = record.product_uom_qty
                elif record.product_uom.uom_type == 'bigger':
                    qty_uom = record.product_uom_qty * record.product_uom.factor_inv
                elif record.product_uom.uom_type == 'smaller':
                    qty_uom = record.product_uom_qty / record.product_uom.factor

                price_unit_with_discount = record.price_unit * (1 - record.discount / 100)
                if price_unit_with_discount / qty_uom > lst_price:
                    discount = 0
                else:
                    discount = (1 - (price_unit_with_discount / qty_uom / lst_price)) * 100
            record.lst_price_discount = discount

    lst_price_discount = fields.Monetary('Discount', currency_field='currency_id',
                                         store=False, compute="get_lst_price_discount")

    @api.depends('product_id')
    def get_price_unit_cost(self):
        for record in self:
            puc = 0
            if record.product_uom.uom_type == 'reference':
                puc = record.product_id.standard_price
            elif record.product_uom.uom_type == 'bigger':
                puc = record.product_id.standard_price * record.product_uom.factor_inv
            elif record.product_uom.uom_type == 'smaller':
                puc = record.product_id.standard_price / record.product_uom.factor
            record['price_unit_cost'] = puc
    price_unit_cost = fields.Monetary('Cost Price', currency_field='currency_id', store=False, compute="get_price_unit_cost")

    @api.depends('product_id')
    def get_udo_cost_amount(self):
        for record in self:
            udo_cost = 0
            for li in record.udo_line_ids:
                udo_cost += li.price_unit_cost * li.product_uom_qty
            record['udo_cost_amount'] = udo_cost

    udo_cost_amount = fields.Monetary('Cost amount', currency_field='currency_id', store=False,
                                      compute="get_udo_cost_amount")

    udo_qty = fields.Integer('Udo Qty')

    def action_open_sol(self):
        return {
            'name': _('SOL'),
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'type': 'ir.actions.act_window',
            'view_id':
                self.env.ref('sale_udo.sale_order_line_udo_form').id,
            'context': dict(self.env.context),
            'target': 'new',
            'res_id': self.id,
        }
