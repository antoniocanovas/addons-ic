# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas <antonio.canovas@ingenieriacloud.com>
#    Pedro josé Baños Guirao <pedro@serincloud.com>
##############################################################################
from odoo import api, fields, models, _


class Roi(models.Model):
    _name = "roi"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Return of investment"

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Commercial',
        default=lambda self: self.env.user,
    )
    set_id = fields.Many2one(
        'roi.set',
        string='Template',
    )
    sale_id = fields.Many2one(
        'sale.order',
        string='Sale',
    )
    contract_id = fields.Many2one(
        'contract.contract',
        string='Contract',
    )
    date_start = fields.Date(string='Start date')
    date_end = fields.Date(string='End date', tracking=True)
    date_roi = fields.Date(string='ROI date', tracking=True, store=True, readonly=True)

    def get_balance_today(self):
        for record in self:
            total = 0
            for li in record.line_ids:
                total += li.agregate
            record.balance_today = total
    balance_today = fields.Monetary(string='Balance', currency_field='currency_id', compute='get_balance_today', store=False)

    balance_global = fields.Monetary(string='Margin', tracking=True, currency_field='currency_id', store=True, readonly=True)
    line_ids = fields.One2many('roi.line', 'roi_id', string='Roi Line')
    currency_id = fields.Many2one('res.currency', string='Currency', default=1)
