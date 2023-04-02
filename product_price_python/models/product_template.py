
from datetime import datetime
import pytz
from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    tipo_calculo        = fields.Selection([('personal', 'Servicios en horario habitual, extra y festivo')],
                                           string='Tipo', store=True, copy=True)
    inicio_jornada      = fields.Float(string="Inicio Jornada")
    final_jornada       = fields.Float(string="Inicio Jornada")
    hextra_inicio       = fields.Float(string="Inicio H. Extras")
    hextra_limite       = fields.Float(string="H. Extra límite")
    hextra_percent      = fields.Float(string="H. Extra  inc.")
    hfestivo_percent    = fields.Float(string="H. Festivo inc.")
