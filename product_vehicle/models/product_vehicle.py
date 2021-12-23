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
    vehicle_date2 = fields.Date(string="2ª Matriculación")
    vehicle_model_id = fields.Many2one("fleet.vehicle.model", string="Model")
    vehicle_brand_id = fields.Many2one("fleet.vehicle.model.brand",
                                       related="vehicle_model_id.brand_id",
                                       string="Brand")
    vehicle_category_id = fields.Many2one("fleet.vehicle.category", string="Category")
    vehicle_id = fields.Many2one("fleet.vehicle", string="My company car")

    vehicle_energy = fields.Selection(selection=TYPE, string="Energy type")
    vehicle_color = fields.Char(string="Color")
    vehicle_power = fields.Char(string="Power")
    vehicle_door = fields.Char(string="Doors")
    vehicle_next_itv = fields.Date(string="Next ITV")
    vehicle_chasis = fields.Char(string="Chasis")
    vehicle_description = fields.Text(string="Description")

    vehicle_supplier = fields.Many2one('res.partner', string="Proveedor")
    vehicle_estimation_ids = fields.One2many('product.vehicle.estimation', 'product_vehicle_id', string="Estimation")
    vehicle_serie_id = fields.Many2one('fleet.vehicle.serie')
    vehicle_price = fields.Float(string="Price", store=True)
    vehicle_rebu_amount = fields.Float(string="REBU Amount", store=True)
    vehicle_is_rebu = fields.Boolean(string='Is REBU')

    @api.depends('vehicle_estimation_ids')
    def get_total_estimations(self):
        for record in self:
            total = 0
            for line in record.vehicle_estimation_ids:
                if not line.invoiced:
                    total += line.amount
            record.vehicle_subtotal_estimation = total

    vehicle_subtotal_estimation = fields.Float(string="Total estimation", store=False, compute="get_total_estimations")

    def get_total_analytic(self):
        for record in self:
            total = 0
            lines = self.env['account.analytic.line'].search([(
                'account_id', 'in', [record.income_analytic_account_id.id, record.expense_analytic_account_id.id])])

            for line in lines:
                if not (line.product_id.product_tmpl_id.id == record.id) and (
                        line.move_id.move_id.move_type in ['out_invoice', 'out_refund']):
                    total += line.amount
            record.vehicle_subtotal_analytic = total
    vehicle_subtotal_analytic = fields.Float(string="Total Analytic", store=False, compute="get_total_analytic")

    @api.depends('vehicle_price', 'vehicle_is_rebu', 'vehicle_rebu_amount')
    def get_vehicle_rebu_iva(self):
        for record in self:
            tax = 0
            if record.vehicle_is_rebu = True:
                tax = (record.vehicle_price + record.vehicle_rebu_amount) * 0.21
            else:
                tax = record.vehicle_price * 0.21
            record.vehice_rebu_iva = tax
    vehicle_rebu_iva = fields.Float(string="REBU/IVA (€)", store=True, compute="get_vehicle_rebu_iva")

    @api.depends('vehicle_estimation_ids', 'vehicle_price', 'supplier_taxes_id')
    def get_vehicle_margin(self):
        for record in self:
            price = record.vehicle_price
            estimations = record.vehicle_subtotal_estimation
            analytics = record.vehicle_subtotal_analytic
            record.vehicle_margin = price + estimations + analytics + record.vehicle_rebu_iva
    vehicle_margin = fields.Float(string="Margin (€)", store=True, compute="get_vehicle_margin")

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


