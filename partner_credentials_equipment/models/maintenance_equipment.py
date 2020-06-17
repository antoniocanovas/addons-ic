# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class MaintenanceEquipmentCredentials(models.Model):
    _inherit = 'maintenance.equipment'

    credentials_ids = fields.One2many('partner.credentials', 'equipment_id')
