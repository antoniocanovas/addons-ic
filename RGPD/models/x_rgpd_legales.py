# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_legales(models.Model):
    _name= "x_rgpd_legales.data"
    _description = "RGPD LEGAL"

    id = fields.Integer()
    x_codigo = fields.Integer()
    x_name= fields.Char(String="string Demo", required=True)
    x_estado = fields.Boolean(String="Estado")
