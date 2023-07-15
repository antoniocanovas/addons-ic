# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class WpTemplate(models.Model):
    _name = 'wp.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'WP Template'

    name = fields.Char('name', store=True, required=True)
    active = fields.Boolean('Active', store=True, default=True)
    wp_pico = fields.Float('Watio pico', store=True, copy=True)
    wp_hour = fields.Float('Watio hora', store=True, copy=True)
    wp_margin = fields.Float('Margin', store=True, copy=True)
    wp_charger_margin = fields.Float('Watio hora', store=True, copy=True)
    line_ids = fields.One2many('wp.template.line', 'wp_template_id', string='Lines', store=True)