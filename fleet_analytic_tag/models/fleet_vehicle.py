from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FleetVehicleTag(models.Model):
    _inherit  = 'fleet.vehicle'

    analytic_tag_id  = fields.Many2one('account.analytic.tag', string='Etiquete analítica')


    @api.multi
    def _analytic_line(self):
        for record in self:
            tag = record.analytic_tag_id.id
            lines = self.env['account.analytic.line'].search([('tag_ids', 'ilike', tag)]).ids
            record['analytic_line_ids'] = [(6, 0, lines)]

    analytic_line_ids = fields.Many2many('account.analytic.line',store=False,readonly=True,compute=_analytic_line, string='Línea analítica')