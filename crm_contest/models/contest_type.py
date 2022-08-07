# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ContestType(models.Model):
    _name = 'contest.type'
    _description = 'Types of contest'

    name = fields.Char(string='Name')

