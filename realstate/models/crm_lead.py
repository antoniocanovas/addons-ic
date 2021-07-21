# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


# (anuncios en portales)
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    realstate_id = fields.Many2one('realstate.property', string='Realstate')

