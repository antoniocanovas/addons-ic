# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ContestContractType(models.Model):
    _name = 'contest.contract.type'
    _description = 'Contest contract types'

    name = fields.Char(string='Name')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)

