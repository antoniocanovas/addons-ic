# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_project(models.Model):
    _inherit= "project.task"



    x_medida_id= fields.Many2many('x_rgpd_medidas', string="Medidas")
    x_rat_id = fields.Many2many('x_rgpd_rats', string="Rats")


