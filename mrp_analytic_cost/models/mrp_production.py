# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    analytic_line_id = fields.Many2one('account.analytic.line', readonly=True, string='Analytic line')

    def get_analytic_cost(self):
        total = 0
        for record in self:
            for li in record.move_raw_ids:
                total += li.quantity_done * li.product_id.standard_price
        for li in record.workorder_ids:
            total += li.workcenter_id.costs_hour * li.duration / 60
        record['analytic_cost'] = total

    analytic_cost = fields.Float('Analytic cost', compute=get_analytic_cost)
