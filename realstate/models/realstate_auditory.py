# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api

class RealstateAuditory(models.Model):
     _name = 'realstate.auditory'
     _description = 'Realstate Audiitory Model'

     name = fields.Char('Visita de captación')
     property_id = fields.Many2one(realstate.property='auditory_ids')


