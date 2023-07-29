# -*- coding: utf-8 -*-
from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def name_get(self):
        print("DEBUG1", self)
        orig_name = super(ResPartner, self).name_get()
        result = []
        if self.env.context.get('origin') == 'sale_order':
            print("DEBUG2")

            for record in self:
                pt = self.env['product.product'].search([('id', '=', self.env.context.get('default_product'))])
                print(record.name, record.id)
                print("record", record.id,  pt.product_tmpl_id.id, )
                product_info = self.env['product.supplierinfo'].search([
                    ('partner_id', '=', record.id),
                    ('product_tmpl_id', '=', pt.product_tmpl_id.id)
                ])
                print("PINFO", product_info)
                fecha_descuento = ''
                if(product_info.date_start):
                    fecha_descuento = product_info.date_start
                result.append((record.id, "%s %s %s %s" % (product_info.display_name, product_info.price, product_info.discount, fecha_descuento)))
            return result
        return orig_name

        # FUNCION QUE DETECTA QUE SE ACCEDE AL CAMPO Y APLICA UN DOMAIN EN FUNCION DE UN VALOR DEL FORMULARIO PADRE

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('origin') == 'sale_order':
            proveedores = []
            pt = self.env['product.product'].search([('id', '=', self.env.context.get('default_product'))])
            proveedores = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', pt.product_tmpl_id.id)])#
            #FALTA ORDERNAR POR display_name
            args = [
                ('id', 'in', proveedores.ids)
            ]
            print(proveedores.mapped('display_name'))
        return super(ResPartner, self).name_search(name, args, operator, limit)
