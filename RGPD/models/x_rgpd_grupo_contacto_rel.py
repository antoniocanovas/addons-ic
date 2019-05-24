# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_grupo_contacto_rel(models.Model):
    _name= "x_rgpd_grupo_contacto_rel"
    _description = "RGPD rel"


    x_name= fields.Char(string="Name")
    # Queda pendiente poner x_name = nombre_grupo + " => " + nombre_contacto !! y además que no sea almacenado.
    x_grupo_id= fields.Many2one('x_rgpd_grupos')
    x_contacto_id = fields.Many2one('res.partner')
    x_empresa_id = fields.Many2one('res.partner',related='x_contacto_id.parent_id',stored=False,string='Empresa')


