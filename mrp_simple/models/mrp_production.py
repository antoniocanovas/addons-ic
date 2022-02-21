# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.production"

    group_id = fields.Many2one('mrp.bom.group', string='Group')
    timesheet_ids = fields.One2many('account.analytic.line', 'mrp_id', string='Timesheets')
    group_id = fields.Many2one('mrp.bom.group', string='Tipo de trabajo')
    bom_easy_id = fields.Many2one('mrp.bom', string='Receta')



