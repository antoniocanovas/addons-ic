# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_product_aternative_ids = fields.Many2many('product.template', string='Last alternative products', store="True",)
