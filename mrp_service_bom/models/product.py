# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

class ProductProduct(models.Model):
        _inherit = "product.product"

    service_bom_id = fields.Many2one('mrp.bom', string="Bill of service",
                                     domain="[('product_tmpl_id', '=', product_tmpl_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                     )
