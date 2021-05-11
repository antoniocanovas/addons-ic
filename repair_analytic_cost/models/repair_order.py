# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    analytic_line_id = fields.Many2one('account.analytic.line', readonly=True, string='Analytic line')

    def get_analytic_cost(self):
        total = 0
        for record in self:
            for li in record.operations:
                if li.type == 'add':
                    total += li.product_uom_qty * li.product_id.standard_price
            for li in record.fees_lines:
                total += li.product_uom_qty * li.product_id.standard_price
            record['analytic_cost'] = total

    analytic_cost = fields.Float('Analytic cost', compute=get_analytic_cost)
