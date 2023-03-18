# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def update_variants_from_price_bom(self):
        for product in self.product_variant_ids:
            if product.price_bom_id.id:
                lst_price, standard_price = 0, 0
                for li in product.price_bom_id.bom_line_ids:
                    lst_price += li.product_id.lst_price * li.product_qty
                    standard_price += li.product_id.standard_price * li.product_qty
                if product.price_bom_id.product_qty not in [0,1]:
                    lst_price = lst_price / product.price_bom_id.product_qty
                    standard_price = standard_price / product.price_bom_id.product_qty
                product.write({'lst_price':lst_price, 'standard_price':standard_price})

class ProductProduct(models.Model):
    _inherit = "product.product"

    price_bom_id = fields.Many2one('mrp.bom', string='Pricing BOM', store=True,
                                     domain="[('product_tmpl_id', '=', product_tmpl_id)]")

    @api.onchange('price_bom_id')
    def update_sale_price_from_service_bom(self):
        lst_price, standard_price = 0, 0
        if self.price_bom_id.id:
            for li in self.price_bom_id.bom_line_ids:
                lst_price += li.product_id.lst_price * li.product_qty
                standard_price += li.product_id.standard_price * li.product_qty
            if self.price_bom_id.product_qty not in [0,1]:
                lst_price = lst_price / self.price_bom_id.product_qty
                standard_price = standard_price / product.price_bom_id.product_qty
        self.write({'lst_price': lst_price, 'standard_price':standard_price})
