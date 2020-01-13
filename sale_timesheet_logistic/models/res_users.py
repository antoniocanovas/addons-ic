from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    fleet_vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='License Plate',
    )
