# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MrpBomGorup(models.Model):
    _name = "mrp.bom.group"
    _description = ""

    name = fields.Char(string='Name', required=True)

