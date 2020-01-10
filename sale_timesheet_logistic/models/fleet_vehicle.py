from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    cost_per_km = fields.Float(
        string='Cost/km',
    )
