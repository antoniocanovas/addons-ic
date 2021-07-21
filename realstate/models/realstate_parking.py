# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class RealstateParking(models.Model):
    _name = 'realstate.parking'
    _description = 'Realstate Parking Model'

    name = fields.Char('Name',  required=True)
