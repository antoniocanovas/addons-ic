# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Contest(models.Model):
    _name = 'contest'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contests'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean('Active', default=True)
    advise_url = fields.Char(string='URL')
    customer_id = fields.Many2one('res.partner', required=True)
    date = fields.Datetime(string='Publication date')
    date_limit = fields.Datetime(string='Expiration')
    place = fields.Char(string='Ubication')
    contractor = fields.Char('Contractor')
    opportunity_id = fields.Many2one('crm.lead')
    advise_file = fields.Binary(string='Advise')
    competitor_num = fields.Integer(string='Competitors')

    user_id = fields.Many2one('res.users', related='opportunity_id.user_id', string='Salesperson')
    competitor_ids = fields.One2many('contest.competitor', 'contest_id', string='Competitors')
    winner_id = fields.Many2one('contest.competitor', string='Winner')

    type_id = fields.Many2one('contest.type', string='Type')
    category_id = fields.Many2one('contest.category', string='Category')
    contract_type = fields.Many2one('contest.contract.type', string='Contract')

    max_price = fields.Monetary(string='Max. Price')
    winner_price = fields.Monetary(string='Adjudication', related='winner_id.price')
    min_price = fields.Monetary('Min.Price')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', store=True, default=1)

    lowerprice_allowed = fields.Boolean(string='Lower price allowed')
    cost_evaluation = fields.Float(string='Economical Evaluation')
    project_evaluation = fields.Float(string='Technical Evaluation')

    note = fields.Text(string='Note')


    cloud_doc = fields.Char('Cloud Doc')
    cloud_folder = fields.Char('Cloud Folder')

    #def _calculate_discount_percent(self):
    #    if self.amount_max & self.amount_winner:
    #        discount_percent = self.amount_max - self.amount_winner
    discount_percent = fields.Float(string='Discount %' )#compute=_calculate_discount_percent)

    def _get_competitor_count(self):
        self.competitor_count = len(self.competitor_ids)

    competitor_count = fields.Integer('Attachments', compute=_get_competitor_count, store=False)

