# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_medidas(models.Model):
    _name= "x_rgpd_medidas.data"
    _description = "RGPD Medidas"


    x_name= fields.Char(String="string Demo", required=True)
    # Multicompañia pendiente
    #x_empresa_id= fields.Many2one('res.partner', 'Empresa' , domain[('is_company','=',True)])
    x_tipo = fields.Selection(['técnicas','legales','organizativas'])
    x_descripcion = fields.Text()
    x_proyecto_id = fields.Many2one('project.project')
    x_usuario_id = fields.Many2one('res.users')
    x_estado = fields.Selection(['Borrador','Activo','Archivado'])

