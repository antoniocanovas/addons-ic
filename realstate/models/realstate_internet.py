# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class RealstateInternet(models.Model):
    _name = 'realstate.internet'
    _description = 'Realstate Internet Model'

    name = fields.Char('Name')
