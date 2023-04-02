from odoo import _, api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    festivos         = fields.Text(string="Festivos")
    festivo_domingo  = fields.Boolean('Festivo el domingo')
