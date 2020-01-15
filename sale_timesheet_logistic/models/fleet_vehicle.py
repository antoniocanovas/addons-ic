from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    cost_per_km = fields.Float(
        string='Cost/km',
    )
    authorized_driver_ids = fields.Many2many(
        comodel_name='res.users',
        relation='fleet_vehicle_res_users_rel',
        column1='fleet_vehicle_id',
        column2='user_id',
        string='Authorized Drivers',
    )
