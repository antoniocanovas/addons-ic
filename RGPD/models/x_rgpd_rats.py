# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class x_rgpd_rats(models.Model):
    _name = "x_rgpd_rats"
    _description = "RGPD rats"

    x_name = fields.Char(String="string Demo", required=True)
    x_rango_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo.x_codigo','=','rango')])



