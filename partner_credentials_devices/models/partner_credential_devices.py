# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredentialDevices(models.Model):
    _name = 'partner.credential.devices'
    _description = 'Devices Tab for partner credentials'

    name = fields.Char(string='Name')
    type_id = fields.Many2one('device_types', string='Type')
    url = fields.Char('IP/URL')
    date_start = fields.Date(string='Registration')
    date_end = fields.Date(string='Renovation')
    note = fields.Text(string='Notes')


