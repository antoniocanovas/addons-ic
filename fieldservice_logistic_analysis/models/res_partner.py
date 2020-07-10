from odoo import fields, models, api, _


class ResPartnerKm(models.Model):
    _inherit = 'res.partner'



    km2origin = fields.Integer(
        'Km desde central'
    )
