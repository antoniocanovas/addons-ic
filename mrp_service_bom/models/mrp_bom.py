# Copyright 2023 Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    product_tmpl_id = fields.Many2one('product.template',
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                      )
    product_id = fields.Many2one('product.product',
                                 domain="[('product_tmpl_id', '=', product_tmpl_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 )
