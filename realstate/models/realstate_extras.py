# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class RealstateExtras(models.Model):
    _name = 'realstate.extras'
    _description = 'Realstate Extras Model'

    name = fields.Char('Name', required=True)

