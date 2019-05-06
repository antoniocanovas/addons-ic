# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_medidas(models.Model):
    _name= "x_rgpd_medidas.data"
    _description = "RGPD Medidas"


    x_name= fields.Char(String="string Demo", required=True)
    x_empresa_id= fields.Integer()
    x_tipo = fields.Selection(['técnicas','legales','organizativas'])
    x_descripcion = fields.Text()
    x_proyecto_id =
    x_usuario_id =
    x_estado = fields.Boolean(String="Estado")

