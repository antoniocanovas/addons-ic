# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contest_competitor_ids = fields.One2many('contest.competitor', 'customer_id')
    contest_competitor_partner_ids = fields.One2many('contest.competitor', 'partner_id')

    def _get_contest_count(self):
        self.contest_count = len(self.contest_competitor_ids)

    contest_count = fields.Integer('Competitors', compute=_get_contest_count, store=False)

    def _get_competitor_count(self):
        self.competitor_count = len(self.contest_competitor_partner_ids)

    competitor_count = fields.Integer('Competitors', compute=_get_competitor_count, store=False)

