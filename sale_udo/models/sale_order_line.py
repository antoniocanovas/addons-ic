from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name = fields.Char(string='Name')
    udo_template_id = fields.Many2one('udo.template', string='UDO Template')
    udo_line_ids = fields.One2many('udo.line', 'sale_line_id', string='UDO Line')

    def get_udo_cost_amount(self):
        cost = 0
        for line in self.udo_line_ids:
            cost += line.price_unit_cost * line.product_uom_qty
        self.udo_cost_amount = cost

    udo_cost_amount = fields.Monetary('UDO Cost', store=False, compute='get_udo_cost_amount')

    def action_open_sol(self):
        return {
            'name': _('SOL'),
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'type': 'ir.actions.act_window',
            'view_id':
                self.env.ref('sale_udo.sale_order_line_udo_form').id,
            'context': dict(self.env.context),
            'target': 'new',
            'res_id': self.id,
        }
