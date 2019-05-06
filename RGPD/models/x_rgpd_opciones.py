# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_opciones(models.Model):
    _name= "x_rgpd.opciones"
    _description = "RGPD Opciones"


    x_name= fields.Char(String="string Demo", required=True)
    #x_empresa_id= fields.Integer()
    x_tipo_id = fields.Many2one('x_rgpd_legales', domain=[('x_estado','=','activo')])
    #x_medida_ids = fields.Many2many('x_rgpd_medidas', domain=[('x_estado','=','activo')])
    x_clausula_informativa = fields.Text()
    x_clausula_tratamiento = fields.Text()
    #x_estado = fields.Selection([('borrador','Borrador'),('activo','Activo'),('archivado','Archivado')])

