# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class RealstateHeating(models.Model):
    _name = 'realstate.heating'
    _description = 'Realstate Heating Model'

    name = fields.Char('Name')
