from odoo import fields, models, api, _


class LogisticFleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'


    cost_per_km = fields.Float('Coste/KM')
    
    analytic_id = fields.Many2one(
        comodel_name='account.analytic.line',
        string='Anlytic Account',
