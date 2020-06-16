# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class DeviceTypes(models.Model):
    _name = 'device.types'
    _description = 'Device Types for credential devices'

    name = fields.Char(string='Name')