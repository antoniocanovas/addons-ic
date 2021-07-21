# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


# (anuncios en portales)
class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    realstate_id = fields.Many2one('realstate.property', string='Realstate')

