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
from datetime import datetime, date, timedelta

TYPE = [
    ('unique', 'Unique'),
    ('monthly', 'Monthly'),
    ('quarted', 'Quarted'),
    ('anual', 'Anual'),
]
class RoiLine(models.Model):
    _name = "roi.line"
    _description = "ROI line"

    name = fields.Char(string='Name')
    roi_id = fields.Many2one('roi', string='ROI')
    sale_id = fields.Many2one(
        'sale.order',
        related='roi_id.sale_id',
        string='Sale',
    )
    contract_id = fields.Many2one(
        'contract.contract',
        related='roi_id.contract_id',
        string='Contract',
    )
    type = fields.Selection(
        selection=TYPE, string="Type", default='unique',
    )
    date_init = fields.Date(string='Start')
    currency_id = fields.Many2one('res.currency', string='Currency')
    qty = fields.Float(string="Quantity")
    amount = fields.Monetary(string="Amount",currency_field='currency_id')
    def get_agregate_roi_line(self):
        for record in self:
            total, today = 0, date.today()
            if record.date_init <= today:
                mtoday = ((today.year - 2001) * 12) + today.month
                start = record.date_init
                mstart = ((start.year - 2001) * 12) + start.month
                dif = mtoday - mstart + 1
                if record.type == 'unique':
                    total += record.qty * record.amount
                elif record.type == 'monthly':
                    total += record.qty * record.amount * dif
                elif record.type == 'quarted':
                    total += record.qty * record.amount * round(dif / 3 + 0.5, 0)
                else:
                    total += record.qty * record.amount * round(dif / 12 + 0.5, 0)
            record.agregate = total
    agregate = fields.Monetary(string="Agregate", compute='get_agregate_roi_line', currency_field='currency_id', store=False)
    date_roi = fields.Date(string='ROI date', compute='get_date_roi')



    sequence = fields.Integer(string="Sequence")