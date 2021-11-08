from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_vehicle = fields.Boolean('Vehicle')

    vehicle_km = fields.Integer(string='KM')
    vehicle_date = fields.Date(string="Date")
    vehicle_model_id = fields.Many2one("fleet.vehicle.model", string="Model")
    vehicle_brand_id = fields.Many2one("fleet.vehicle.model.brand",
                                       related="vehicle_model_id.brand_id",
                                       string="Model")
    vehicle_category_id = fields.Many2one("fleet.vehicle.category", string="Category")
    vehicle_id = fields.Many2one("fleet.vehicle", string="ID")

    def get_opp_ids(self):
        for record in self:
            ops = self.env['crm.lead'].search([('vehicle_ids', 'like', record.id)]).ids
            record.opportunity_ids = [(6, 0, ops)]
    opportunity_ids = fields.Many2many('crm.lead', string="Opportunities", readonly=True, compute="get_opp_ids")


