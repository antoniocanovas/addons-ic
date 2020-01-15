from odoo import fields, models , api


class ResUsers(models.Model):
    _inherit = 'res.users'

    vehicle_ids = fields.Many2many(
            comodel_name='fleet.vehicle',
            relation='fleet_vehicle_res_users_rel',
            column1='user_id',
            column2='fleet_vehicle_id',
            string='Vehicles',
    )