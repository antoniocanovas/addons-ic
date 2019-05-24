# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_medidas(models.Model):
    _name= "x_rgpd_medidas"
    _description = "RGPD Medidas"


    x_name= fields.Char(string="Name", required=True)
    # Multicompañia pendiente
    x_empresa_id= fields.Many2one('res.partner',string='Empresa' , domain=[('is_company','=',True)])
    x_tipo = fields.Selection(selection=[('legal','Legal'),('tecnica','Técnica'),('organizativa','Organizativa')],string='tipo')
    x_descripcion = fields.Text(string='Descripción')
    x_proyecto_id = fields.Many2one('project.project',string='Proyecto')
    x_usuario_id = fields.Many2one('res.users',string='Usuario')
    x_estado = fields.Selection(selection=[('borrador','Borrador'),('activo','Activo'),('archivado','Archivado')],string="Estado",default='activo')

