# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_grupo_contacto_rel(models.Model):
    _name= "x_rgpd_grupo_contacto.rel"
    _description = "RGPD rel"


    x_name= fields.Char(String="string Demo", required=True)
    x_grupo_id= fields.Many2one('x_rgpd_grupos')
    x_contacto_id = fields.Many2one('res.partner')


