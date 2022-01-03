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
    price_control = fields.Boolean(string='Price Control', get='get_price_control')

    @api.depends('product_id')
    def get_standard_price(self):
        for record in self:
            record.standard_price = record.product_id.standard_price
    standard_price = fields.Float(string='Standard Price', store=True, compute="get_standard_price")

    def update_product_standard_price(self):
        for record in self:
            #product = record.product_id
            #product['standard_price'] = record.price_unit
            record.product_id.standard_price = record.price_unit
            print("Object,", record.product_id,)


    @api.onchange('price_unit')
    def price_unit_wizard(self):
        if self.price_unit != self.standard_price:
            message = "Precio de coste actual: " + str(self.standard_price) + ". Pulsa el botón para actualizar."
            return {
                'warning': {
                    'title': 'Standard price and Price unit is not the same!',
                    'message': message,
                }
            }

            #return {
            #    'name': _("Price is not the same!"),
            #    'type': 'ir.actions.act_window',
            #    'view_type': 'form',
            #    'view_mode': 'form',
            #    'res_model': 'price.unit.info',
            #    'view_id': view_id,
            #    'target': 'new',
            #    'context': {
            #        'purchase_order_id': self.id,
            #        'message': message,
            #    }
            #}