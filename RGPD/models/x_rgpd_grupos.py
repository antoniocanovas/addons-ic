# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_grupos(models.Model):
    _name= "x_rgpd.grupos"
    _description = "RGPD Opciones"


    x_name= fields.Char(String="string Demo", required=True)
    x_contacto_ids= fields.Many2many('res.partner', domain=[('is_company','=',False)])
    #x_estado = fields.Selection([('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')])


