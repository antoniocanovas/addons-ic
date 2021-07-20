# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class RealstateCooling(models.Model):
    _name = 'realstate.cooling'
    _description = 'Realstate Air Cooling'

    name = fields.Char('Name')
