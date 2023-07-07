# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    set_template_ids = fields.Many2many('set.template', string='Set templates', store="True",)
