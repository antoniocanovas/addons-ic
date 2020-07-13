from odoo import fields, models, api


class FsmOrderLogistic(models.Model):
    _inherit = 'sale.order.line'

    #@api.multi
    #def recalculate_margin(self, id, amount):
    #        sale_order_line = self.env['sale.order.line'].sudo().search([("id", "=", id)])

    #        sale_order_line.margin = float(amount)

