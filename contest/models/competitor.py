# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Competitor(models.Model):
    _name = 'competitor'
    _description = 'Competitor fileds'

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner')
    contest_id = fields.Many2one('contest')
    opportunity_id = fields.Many2one('crm.lead', related='contest_id.opportunity_id')
    customer_id = fields.Many2one('res.partner', related='contest_id.customer_id')
    type = fields.Many2one('contest.type', related='contest_id.type_id')
    category = fields.Many2one('contest.category', related='contest_id.category_id')
    contract = fields.Many2one('contest.contract.type', related='contest_id.contract_type')

    amount = fields.Float('Amount')
    note = fields.Text('Note')

    @api.depends('contest_id.winner_id')
    def get_winner(self):
        for record in self:
            winner = False
            if record.contest_id.winner_id.id == record.id: winner = True
            record.winner = winner
    winner = fields.Boolean('Winner', compute=get_winner)

    @api.depends('amount')
    def get_lowerprice(self):
        for record in self:
            lowerprice = False
            if record.contest_id.min_price > record.amount: lowerprice = True
            record.lowerprice = lowerprice
    lowerprice = fields.Boolean('Lowerprice', compute=get_lowerprice)

    @api.depends('amount', 'contest_id.max_price')
    def get_discount(self):
        for record in self:
            discount = 0
            if record.contest_id.max_price > 0:
                discount = 1 - record.amount / record.contest_id.max_price
        record.discount = discount
    discount = fields.Float('Discount', compute=get_discount)
