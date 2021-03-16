# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Contest(models.Model):
    _name = 'contest'
    _description = 'Contests'

    name = fields.Char(string='Name')
    advise_url = fields.Char(string='URL')
    customer_id = fields.Many2one('res.partner')
    date = fields.Datetime(string='Publication date')
    date_limit = fields.Datetime(string='Expiration')
    place = fields.Char(string='Ubication')
    contractor = fields.Char('Contractor')
    opportunity_id = fields.Many2one('crm.lead')
    advise_file = fields.Binary(string='Advise')
    competitor_num = fields.Integer(string='Competitors')

    competitor_ids = fields.One2many('competitor', 'contest_id', string='Competitors')
    winner_id = fields.Many2one('competitor', string='Winner')

    type_id = fields.Many2one('contest.type', string='Type of contest')
    category_id = fields.Many2one('contest.category', string='Category of contest')
    contract_type = fields.Many2one('contest.contract.type', string='Contest contract type')

    max_price = fields.Float(string='Max. Price')
    winner_price = fields.Float(string='Adjudication')

    lowerprice_allowed = fields.Boolean(string='Lowerprice')
    cost_evaluation = fields.Float(string='Economical Evaluation')
    project_evaluation = fields.Float(string='Technical Evaluation')

    note = fields.Text(string='Note')

    min_price = fields.Float('Quotation')
    user_id = fields.Many2one('crm.lead', related='opportunity_id.user_id', string='User')

    cloud_doc = fields.Char('Cloud Doc')
    cloud_folder = fields.Char('Cloud Folder')

    #def _calculate_discount_percent(self):
    #    if self.amount_max & self.amount_winner:
    #        discount_percent = self.amount_max - self.amount_winner
    discount_percent = fields.Float(string='Discount %' )#compute=_calculate_discount_percent)

