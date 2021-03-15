# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Competitor(models.Model):
    _name = 'competitor'
    _description = 'Competitor fileds'

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner')
    contest_id = fields.Many2one('contest')

