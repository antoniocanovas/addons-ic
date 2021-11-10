from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

TYPE = [
    ('gasolina', 'Gasolina'),
    ('diesel', 'Diesel'),
    ('glp', 'GLP'),
    ('electric', 'Eléctrico'),
    ('h_gasoline', 'Híbrido Gasolina'),
    ('h_gasoil', 'Híbrido Gasoil'),
]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_vehicle = fields.Boolean('Vehicle')

    vehicle_km = fields.Integer(string='KM')
    vehicle_date = fields.Date(string="Date")
    vehicle_date2= fields.Date(string="2ª Matriculación")
    vehicle_model_id = fields.Many2one("fleet.vehicle.model", string="Model")
    vehicle_brand_id = fields.Many2one("fleet.vehicle.model.brand",
                                       related="vehicle_model_id.brand_id",
                                       string="Model")
    vehicle_category_id = fields.Many2one("fleet.vehicle.category", string="Category")
    vehicle_id = fields.Many2one("fleet.vehicle", string="ID")

    rebu = fields.Boolean(string="Rebu")
    vehicle_energy = fields.Selection(selection=TYPE, string="Energy type")
    vehicle_color = fields.Char(string="Color")
    vehicle_power = fields.Char(string="Power")
    vehicle_door = fields.Char(string="Doors")
    vehicle_next_itv = fields.Date(string="Next ITV")
    vehicle_chasis = fields.Char(string="Chasis")

    vehicle_supplier = fields.Many2one('res.partner', string="Proveedor")
    vehicle_estimation_ids = fields.One2many('product.vehicle.estimation', 'product_vehicle_id', string="Estimation")

    vehicle_total_estimation = fields.Float(string="Total estimation")

    vehicle_total_analityc = fields.Float(string="Total Analityc")

    vehicle_margin = fields.Float(string="Margin")

    vehicle_price = fields.Float(string="Total price")

    def get_analytic_lines(self):
        for record in self:
            lines = self.env['account.analytic.line'].search([(
                'account_id', 'in', [record.income_analytic_account_id.id, record.expense_analytic_account_id.id])])
            record.analytic_line_ids = [(6, 0, lines.ids)]
    analytic_line_ids = fields.Many2many('account.analytic.line', store=False, Readonly=True, string="Analytic",
                                         compute="get_analytic_lines")

    def get_opp_ids(self):
        for record in self:
            ops = self.env['crm.lead'].search([('vehicle_ids', 'like', record.id)]).ids
            record.opportunity_ids = [(6, 0, ops)]
    opportunity_ids = fields.Many2many('crm.lead', string="Opportunities", readonly=True, compute="get_opp_ids")


