# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_grupo_x_rgpd_rats_rel(models.Model):
    _name= "x_rgpd_grupo_x_rgpd_rats_rel"
    _description = "RGPD rel grupos_rats"


    x_name= fields.Char(string="Name")
    x_rgpd_grupos_id= fields.Many2one('x_rgpd_grupos')
    x_rgps_rats_id = fields.Many2one('x_rgpd_rats')



