# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2020 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models, _

class Roi(models.Model):
    _name = "roi"
    _description = "Return of investment"

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Commercial',
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
    date_end = fields.Date(string='End date')
    date_roi = fields.Date(string='ROI date', store=True, readonly=True)

    def get_balance_today(self):
        for record in self:
            total = 0
            for li in record.line_ids:
                total += li.agregate
            record.balance_today = total
    balance_today = fields.Monetary(string='Balance', currency_field='currency_id', compute='get_balance_today', store=False)

    line_ids = fields.One2many('roi.line', 'roi_id', string='Roi Line')
    currency_id = fields.Many2one('res.currency', string='Currency', default=1)
