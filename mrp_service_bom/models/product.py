# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def update_variants_sale_price_from_service_bom(self):
        for product in self.product_variant_ids:
            if product.service_bom_id.id:
                list_price = 0
                for li in product.service_bom_id.bom_line_ids:
                    list_price += li.product_id.lst_price * li.product_qty
                if product.service_bom_id.product_qty not in [0,1]:
                    list_price = list_price / product.service_bom_id.product_qty
                product.write({'lst_price':list_price})

class ProductProduct(models.Model):
    _inherit = "product.product"

    service_bom_id = fields.Many2one('mrp.bom', string='Sale BOM price', store=True,
                                     domain="[('product_tmpl_id', '=', product_tmpl_id)]")

    @api.depends('service_bom_id')
    def update_sale_price_from_service_bom(self):
        list_price = 0
        if self.service_bom_id.id:
            for li in self.service_bom_id.bom_line_ids:
                list_price += li.product_id.lst_price * li.product_qty
            if self.service_bom_id.product_qty not in [0,1]:
                list_price = list_price / self.service_bom_id.product_qty
        self.lst_price = list_price
