# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_rgpd_legales(models.Model):
    _name= "x_rgpd_legales"
    _description = "RGPD LEGAL"

    #id = fields.Integer()
    x_codigo = fields.Char(string="Código")
    x_name= fields.Char(string="Name")
    #x_estado = fields.Selection([('borrador','Borrador'),('activo','Activo'),('archivado','Archivado')],string="Estado")
    x_estado = fields.Selection(selection=[('borrador','Borrador'),('activo','Activo'),('archivado','Archivado')],string="Estado",default='activo')
