# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_aternative_product_ids = fields.Many2many(comodel_name='product.template',
#                                                   relation='product_lead_rel',
                                                   relation='product_alternative_rel',
#                                                   column1='product1_id',
#                                                   column2='product2_id',
                                                   string='Last alternative products',
                                                   store="True",)

    last_accesory_product_ids = fields.Many2many(comodel_name='product.template',
                                                   relation='product_accesory_rel',
#                                                   column1='product1_id',
#                                                   column2='product2_id',
                                                   string='Last accesory products',
                                                   store="True",)