
from odoo import api, fields, models


class PntMaintenanceEquipmentModel(models.Model):
    _name = 'pnt.maintenance.equipment.model'
    _description = 'pnt.maintenance.equipment.model'

    name = fields.Char(string="Name")



