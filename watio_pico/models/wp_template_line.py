# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class WpTemplateLine(models.Model):
    _name = 'wp.template.line'
    _description = 'WP Template line'

    name = fields.Char('name', store=True, required=True)
    product_id = fields.Many2one('product.product', store=True, copy=True)
    type = fields.Selection('Type', related='product_id.wp_type', store=False)
    quantity = fields.Float('Quantity', store=True, copy=True)
    factor = fields.Float('Factor', store=True, copy=True)
    wp_template_id = fields.Many2one('wp.template', store=True, reaonly=True, copy=False)
