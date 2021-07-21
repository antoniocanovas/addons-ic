# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


# (murcia centro, playa, …)
class RealstateArea(models.Model):
    _name = 'realstate.area'
    _description = 'Realstate Area Model'

    name = fields.Char('Name',  required=True)
