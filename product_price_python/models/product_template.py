from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo        = fields.Selection([('personal', 'Servicios en horario habitual, extra y festivo')],
                                           string='Tipo', store=True, copy=True)
    inicio_extra        = fields.Integer(string="Inicio Extra")
    inicio_ordinario    = fields.Integer(string="Inicio Ordinaria")
    final_ordinario     = fields.Integer(string="Fin Ordinaria")
    final_hextra        = fields.Integer(string="Hora Extra límite")
    hextra_factor       = fields.Float(string="Factor Hora Extra")
    hfestivo_factor     = fields.Float(string="Factor Festivo")
    horas_minimo        = fields.Integer(string="Horas mínimas")
