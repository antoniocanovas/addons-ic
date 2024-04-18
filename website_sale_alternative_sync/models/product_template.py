# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_product_aternative_ids = fields.Many2many(comodel_name='product.template',
                                                   relation='product_lead_rel',
                                                   column1='product1_id',
                                                   column2='product2_id',
                                                   string='Last alternative products',
                                                   store="True",)
