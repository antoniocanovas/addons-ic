# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'sale.order',

    extra_percent = fields.Float('Extra percent', store=True)
    holiday_percent = fields.Float('Extra percent', store=True)
    standard_begin = fields.Float('Standard begin')
    standard_end   = fields.Float('Standard end')

    def get_update_pricelist(self):
        pricelist = self.user.company_id.property_product_pricelist
        extra = self.extra_percent + self.holiday_percent
        price = self.list_price
        new_price = price * (1 + (extra/100))

        if (not pricelist.id):
            raise UserError('Asigna una tarifa para tu compañía, se usará para actualizar los precios')
        else:
            for li in self.product_variant_ids:
                product_pricelist_line = self.env['product.pricelist.item'].search([('product_id','=',self.id),
                                                                                    ('pricelist_id','=',pricelist.id)])
                if product_pricelist_line.id:
                    product_pricelist_line.id.write({'fixed_price':})
