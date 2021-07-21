# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


# ( 1ª línea de playa, residencial, ...)
class RealstateEnviroment(models.Model):
    _name = 'realstate.enviroment'
    _description = 'Realstate Enviroment Model'

    name = fields.Char('Name',  required=True)
