# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


# (anuncios en portales)
class resCompanyRealState(models.Model):
    _inherit = 'res.company'

    realstate = fields.Boolean(string='Realstate')

