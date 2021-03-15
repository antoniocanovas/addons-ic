# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Contest(models.Model):
    _name = 'contest'
    _description = 'Contests'

    name = fields.Char(string='Name')
    advise_url = fields.Char(string='URL')
    customer_id = fields.Many2one('res.partner')
    publication = fields.Datetime(string='Publication date')
    expiration = fields.Datetime(string='Expiration')
    place = fields.Char(string='Ubication')
    department = fields.Char('Contract department')
    opportunity_id = fields.Char('Opportunity')
    advise = fields.Binary(string='Advise')
    competitor_num = fields.Integer(string='Total competitors')

    competitor_ids = fields.One2many('competitor', 'contest_id', string='Competitors')
    winner_id = fields.Many2one('competitor', string='Winner')

    type = fields.Many2one('contest.type', string='Type of contest')
    category = fields.Many2one('contest.category', string='Category of contest')
    contract_type = fields.Many2one('contest.contract.type', string='Contest contract type')

    amount_max = fields.Float(string='Max. amount')
    amount_winner = fields.Float(string='Winner amount')

    downprice_allowed = fields.Boolean(string='Allow downprice')
    cost_evaluation = fields.Float(string='Economical Evaluation')
    project_evaluation = fields.Float(string='Technical Evaluation')

    note = fields.Text(string='Note')

    def _calculate_discount_percent(self):
        if self.amount_max & self.amount_winner:
            discount_percent = self.amount_max - self.amount_winner
    discount_percent = fields.Float(string='Discount %', compute=_calculate_discount_percent)


