# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class RealstateVisit(models.Model):
    _name = 'realstate.visit'
    _description = 'Realstate Visit Model'

    name = fields.Char('Name',  required=True)
    opportunity_id = fields.Char()
    date = fields.Date()
    property_id = fields.Many2one('realstate.property')
    done = fields.Boolean()
    note = fields.Char()
