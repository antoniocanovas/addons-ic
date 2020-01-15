
from odoo import fields, models , api


class FleetVehicleResUsersRel(models.Model):
    _name = 'fleet.vehicle.res.users.rel'
    _description = 'Relational table for user and vehicles '

    @api.depends('fleet_vehicle_id')
    def _get_vehicle_name(self):
        for record in self:
            record['name'] = record.fleet_vehicle_id.name

    name = fields.Char(string='Name', compute=_get_vehicle_name, readonly=True)

    fleet_vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='License Plate',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
    )