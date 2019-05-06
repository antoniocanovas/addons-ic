# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_opciones(models.Model):
    _name= "x_rgpd.opciones"
    _description = "RGPD Opciones"


    x_name= fields.Char(String="string Demo", required=True)
    x_empresa_id= fields.Integer()
    x_tipo_id = fields.Selection(['técnicas','legales','organizativas'])
    x_medida_ids = fields.Many2one("x_rgpd.legales", String="RGPD_legales")
    x_clausula_informativa = fields.Text()
    x_clausula_tratamiento = fields.Text()
    x_estado = fields.Boolean(String="Estado")

