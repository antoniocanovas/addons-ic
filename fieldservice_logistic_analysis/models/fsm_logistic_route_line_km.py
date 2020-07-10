from odoo import fields, models, api, _


class LogisticRouteLineKm(models.Model):
    _inherit = 'fsm.logistic.route.line'

    @api.multi
    def _compute_profitability(self):
        for record in self:
            total = 0
            for order in record.fsm_order_ids:
                total += order.logistic_margin
            record.logistic_margin = total

    logistic_margin = fields.Float(string='Margen', compute=_compute_profitability, stored=False)

    @api.multi
    def action_km_wizard(self):
        view_id = self.env.ref('fieldservice_logistic_analysis.calculate_km_wizard_view').id

        return {
            'name': _("Reparto Km"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'logistic.analysis.km',
            'view_id': view_id,
            'target': 'new',
            'context': {'default_logistic_route_line_id': self.id},
        }
