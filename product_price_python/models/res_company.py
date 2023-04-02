from odoo import _, api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    festivos         = fields.Text(string="Festivos", placeholder="En formato año-mes-día, separado por comas (2023-12-31)")
    festivo_domingo  = fields.Boolean('Festivo el domingo')
