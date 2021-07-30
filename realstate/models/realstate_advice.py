# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


# (anuncios en portales)
class RealstateAdvice(models.Model):
    _name = 'realstate.advice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Realstate Advice Model'

    name = fields.Char('Name', required=True)
    property_id = fields.Many2one('realstate.property')
    date_begin = fields.Date('Begin date', tracking=True)
    date_end = fields.Date('End date', tracking=True)
    url = fields.Char()
    printed_advice = fields.Binary()

    amount = fields.Monetary(string='Amount', digits=(7, 2), currency_field='currency_id')
    active = fields.Boolean("Active", default=True)
    medium_id = fields.Many2one("utm.medium", string='Medium', tracking=True)
    note = fields.Text(string='Note')

    def get_currency(self):
        self.currency_id = self.env.user.company_id.currency_id

    currency_id = fields.Many2one('res.currency', compute='get_currency')