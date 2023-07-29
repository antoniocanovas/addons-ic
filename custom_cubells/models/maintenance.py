# -*- coding: utf-8 -*-
from odoo import models, api, fields


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    pnt_ot_num = fields.Char(string="OT number")
    pnt_manufacturing_month = fields.Char(string="Manufacturing Month")
    pnt_maintenance_year = fields.Char(string="Maintenance year")
    pnt_burner = fields.Char(string="Burner")
    pnt_legalized = fields.Char(string="Legalized")
    pnt_final_partner = fields.Char(string="Final customer")
    pnt_various1 = fields.Char(string="Various 1")
    pnt_various2 = fields.Char(string="Various 2")
    pnt_various3 = fields.Char(string="Various 3")

    pnt_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer",
        domain="[('is_company','=',1)]"
    )
    pnt_state_id = fields.Many2one(
        comodel_name="res.country.state", string="State"
    )
    pnt_model_id = fields.Many2one(
        comodel_name="pnt.maintenance.equipment.model", string="Model"
    )
    pnt_fuel_id = fields.Many2one(
        comodel_name="pnt.maintenance.equipment.fuel", string="Fuel"
    )


