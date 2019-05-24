# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_opciones(models.Model):
    _name= "x_rgpd_opciones"
    _description = "RGPD Opciones"


    x_name= fields.Char(string="Name", required=True)
    #x_empresa_id= fields.Integer()
    x_tipo_id = fields.Many2one('x_rgpd_legales', domain=[('x_estado','=','activo')],string="Tipo")
    #x_tipo_codigo_id = fields.Char(related='x_tipo_id.x_codigo', string="Código", readonly=True)
    x_medida_ids = fields.Many2many('x_rgpd_medidas', domain=[('x_estado','=','activo')],string="Medidas")
    x_clausula_informativa = fields.Text(string="Clausula Informativa")
    x_clausula_tratamiento = fields.Text(string="Clausula de tratamiento")
    x_estado = fields.Selection(selection=[('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')],
                                string="Estado", default='activo')


