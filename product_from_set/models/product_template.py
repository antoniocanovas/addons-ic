# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    set_template_ids = fields.Many2many('set.template', string='Set templates', store="True",)
    parent_id = fields.Many2one('product.template', string='Parent set', store=True)
    set_product_ids  = fields.One2many('product.template','parent_id', string='Set products', store=True)

