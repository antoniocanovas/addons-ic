
from odoo import api, fields, models


class PntMaintenanceEquipmentFuel(models.Model):
    _name = 'pnt.maintenance.equipment.fuel'
    _description = 'pnt.maintenance.equipment.fuel'

    name = fields.Char(string="Name")



