# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api

# (anuncios en portales)
class RealstateAdvice(models.Model):
     _name = 'realstate.advice'
     _description = 'Realstate Advice Model'

     name = fields.Char('Name')
     property_id = fields.Many2one('realstate.property')
     date_begin = fields.Date('Begin date')
     date_end = fields.Date('End date')
     url = fields.Char()
     attachment = fields.Binary()
     amount = fields.Float(string='Amount', digits=(7,2))


