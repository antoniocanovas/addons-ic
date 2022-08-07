# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    contest_competitor_ids = fields.One2many('contest.competitor', 'opportunity_id')

    def _get_competitor_count(self):
        self.competitor_count = len(self.contest_competitor_ids)

    competitor_count = fields.Integer('Competitors', compute=_get_competitor_count, store=False)

