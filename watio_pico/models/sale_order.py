# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SsaleOrder(models.Model):
    _inherit = 'sale.order'

    is_wp = fields.Boolean('WatioPico')
    wp_power = fields.Float('Power Kw', store=True)
    wp_template_id = fields.Many2one('wp.template', string='WP Template', store=True)
    wp_line_ids = fields.One2many('wp.sale.line', 'sale_id', string='WP Lines')

    @api.onchange('wp_template_id')
    def get_wp_template_margin(self):
        self.wp_margin = self.wp_template_id.wp_margin
    wp_margin = fields.Float('WP Margin', store=True, readonly=False, compute='get_wp_template_margin')

    @api.onchange('wp_template_id')
    def get_wp_charger_template_margin(self):
        self.wp_charger_margin = self.wp_template_id.wp_charger_margin
    wp_charger_margin =  fields.Float('Charger Margin', store=True, readonly=False, compute='get_wp_charger_template_margin')

    @api.onchange('wp_template_id')
    def get_wp_template_lines(self):
        self.wp_line_ids.unlink()
        for li in self.wp_template_id.line_ids:
            newline = self.env['wp.sale.line'].create({'product_id':li.product_id.id,
                                                       'name':li.name,
                                                       'quantity':li.quantity,
                                                       'factor':li.factor,
                                                       'subtotal':0,
                                                       'sale_id':self.id})

    @api.onchange('wp_margin','wp_charger_margin','wp_line_ids')
    def _update_wp_prices(self):
        total = 0
        for li in self.wp_template_id.line_ids:
            # Case watio-pico:
            if li.product_id.wp_type == 'wp':
                subtotal = 1
            # Case watio-hour:
            elif li.product_id.wp_type == 'wh':
                subtotal = 2
            # Case charger:
            else:
                subtotal = 3
            li.subtotal = subtotal
            total += subtotal
        li.wp_total = total

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