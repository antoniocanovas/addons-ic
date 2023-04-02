from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo        = fields.Selection([('personal', 'Servicios en horario habitual, extra y festivo')],
                                           string='Tipo', store=True, copy=True)
    inicio_jornada      = fields.Float(string="Inicio Ordinaria")
    final_jornada       = fields.Float(string="Fin Ordinaria")
    hextra_inicio       = fields.Float(string="Extras mañana desde")
    hextra_limite       = fields.Float(string="H. Extra límite")
    hextra_factor       = fields.Float(string="H. Extra  factor")
    hfestivo_factor     = fields.Float(string="H. Festivo factor")
