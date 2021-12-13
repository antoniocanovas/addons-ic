# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas <antonio.canovas@ingenieriacloud.com>
#    Pedro josé Baños Guirao <pedro@serincloud.com>
##############################################################################
from odoo import api, fields, models, _

TYPE = [
    ('unique', 'Unique'),
    ('monthly', 'Monthly'),
    ('quarted', 'Quarted'),
    ('anual', 'Anual'),
]


class RoiSetLine(models.Model):
    _name = "roi.set.line"
    _description = "ROI Set Line"

    set_id = fields.Many2one(
        'roi.set',
        string='ROI set',
    )
    type = fields.Selection(
        selection=TYPE, string="Type", default='unique',
    )
    currency_id = fields.Many2one('res.currency', string='Currency', default=1)
    amount = fields.Monetary(string="Amount", currency_field='currency_id')
    qty = fields.Integer(string='Quantity')
    name = fields.Char(string='Name')
    sequence = fields.Integer(string="Sequence")
