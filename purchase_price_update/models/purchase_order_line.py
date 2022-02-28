##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class PurchasePriceUpdate(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('standard_price','price_unit')
    def get_price_control(self):
        for record in self:
            control = False
            if record.standard_price == record.price_unit:
                control = True
            record.price_control = control
    price_control = fields.Boolean(string='Price Control', compute='get_price_control')

    @api.depends('product_id')
    def get_standard_price(self):
        for record in self:
            record.standard_price = record.product_id.standard_price
    standard_price = fields.Float(string='Standard Price', store=True, compute="get_standard_price")

    def update_product_standard_price(self):
        for record in self:
            record.product_id.standard_price = record.price_subtotal / record.product_qty

    @api.onchange('price_subtotal')
    def price_unit_wizard(self):
        message = ''
        if self.price_subtotal != 0 and self.product_qty != 0:
            price_unit = self.price_subtotal / self.product_qty
        else:
            price_unit = self.standard_price

        if price_unit != self.standard_price and self.standard_price == 0:
            message = 'Producto sin precio de coste asignado!' + "\n" + 'Recuerde pulsar el botón para asignar este.'

        elif price_unit != self.standard_price and self.standard_price != 0:
            new_pvp = round((self.product_id.lst_price / self.standard_price * price_unit), 2)
            message = "Precio de coste actual: " + str(self.standard_price) + "\n" + "Precio de venta actual: " + str(
                self.product_id.lst_price) + "\n" + "Posible nuevo precio de venta: " + str(
                new_pvp) + "\n" + " !!  Recuerde pulsar el botón para actualizar, si procede el cambio !!"

        if message != '':
            return {
                'warning': {
                    'title': 'Standard price and Price unit is not the same!',
                    'message': message,
                }
            }
