# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SsaleOrder(models.Model):
    _inherit = 'sale.order'

    is_wp = fields.Boolean('WatioPico')
    wp_template_id = fields.Many2one('wp.template', string='WP Template', store=True)

    @api.onchange('wp_template_id')
    def get_wp_template_margin(self):
        self.wp_margin = self.wp_template_id.wp_margin
    wp_margin = fields.Float('WP Margin', store=True, readonly=False, compute='get_wp_template_margin')

    @api.onchange('wp_template_id')
    def get_wp_charger_template_margin(self):
        self.wp_charger_margin = self.wp_template_id.wp_charger_margin
    wp_charger_margin =  fields.Float('Charger Margin', store=True, readonly=False, compute='get_wp_charger_template_margin')

    wp_line_ids = fields.One2many('wp.sale.line', 'sale_id', string='WP Lines')

    @api.depends('wp_line_ids.subtotal')
    def get_wp_subtotal(self):
        for record in self:
            subtotal = 0
            for li in record.wp_line_ids:
                subtotal += li.subtotal
        self.wp_subtotal = subtotal
    wp_subtotal = fields.Monetary('Subtotal', store=True, compute='get_wp_subtotal')

    def update_wp_margin(self):
        return True