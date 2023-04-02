from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo        = fields.Selection([('personal', 'Servicios en horario habitual, extra y festivo')],
                                           string='Tipo', store=True, copy=True)
    hextra_inicio       = fields.Float(string="Inicio Extra")
    inicio_jornada      = fields.Float(string="Inicio Ordinaria")
    final_jornada       = fields.Float(string="Fin Ordinaria")
    hextra_limite       = fields.Float(string="Hora Extra límite")
    hextra_factor       = fields.Float(string="Factor Hora Extra")
    hfestivo_factor     = fields.Float(string="Factor Festivo")
