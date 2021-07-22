# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat_file1 = fields.Binary(
        string='DNI propietario',
    )
    name_vat_file1 = fields.Char(
        string='Nombre Anverso',
    )
    vat_file2 = fields.Binary(
        string='DNI Reverso',
    )
    name_vat_file2 = fields.Char(
        string='Nombre Reverso',
    )




