# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ViafirmaGroups(models.Model):
    _name = 'viafirma.groups'
    _description = 'Viafirma GroupCodes'

    name = fields.Char(
        string='Código de grupo'
    )

