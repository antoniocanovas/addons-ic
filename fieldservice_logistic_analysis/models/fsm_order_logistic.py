from odoo import fields, models, api


class FsmOrderLogistic(models.Model):
    _inherit = 'fsm.order'

    #@api.depends('km')
    #def _get_margin(self):
    #    for record in self:
    #        if not record.sale_line_id:
    #            record.logistic_margin = 0 - (record.km * record.vehicle_id.fleet_vehicle_id.cost_per_km)
    #        else:
    #            this_margin = record.sale_line_id.price_subtotal - record.logistic_route_line_id.fsm_vehicle_id.cost_per_km * record.km
    #            record.logistic_margin = this_margin
    #            record.sale_line_id.recalculate_margin(record.sale_line_id.id, this_margin)

    logistic_margin = fields.Float(string='Margen', readonly=True) # compute=_get_margin)
