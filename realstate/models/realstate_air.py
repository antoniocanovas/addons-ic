# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api

class RealstateAir(models.Model):
     _name = 'realstate.air'
     _description = 'Realstate Air Model'

     name = fields.Char('Name')

