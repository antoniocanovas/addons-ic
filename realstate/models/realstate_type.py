# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api

# (piso, planta baja, dúplex, terreno, cochera, …)
class RealstateType(models.Model):
     _name = 'realstate.type'
     _description = 'Realstate Type Model'

     name = fields.Char('Name')

