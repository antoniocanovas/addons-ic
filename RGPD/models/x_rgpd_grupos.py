# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_grupos(models.Model):
    _name= "x_rgpd_grupos"
    _description = "RGPD Grupos"


    x_name= fields.Char(string="Name", required=True)
    x_contacto_ids = fields.Many2many('res.partner', domain=[('is_company','=',False)],
                                      relation='x_rgpd_grupo_contacto_rel', cloumn1='x_grupo_id' ,clolum2='x_contacto_id', string="Contacto")
    x_empresa_id = fields.Many2many('res.partner', domain=[('is_company', '=', True)])
    #x_grupo_id = fields.Many2many('res.partner', domain=[('is_company', '=', False)])
    x_estado = fields.Selection([('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')])


