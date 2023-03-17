# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_update_sale_price_from_pt(self):
        return(False)

class ProductProduct(models.Model):
    _inherit = "product.product"

    service_bom_id = fields.Many2one('mrp.bom', string='Sale BOM price', store=True,
                                     domain="[('product_tmpl_id', '=', product_tmpl_id)]")

    def _get_update_sale_price_from_pp(self):
        return(False)
