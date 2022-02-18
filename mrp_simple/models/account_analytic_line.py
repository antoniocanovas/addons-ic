# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    mrp_id = fields.Many2one('mrp.production', string='Producción')

