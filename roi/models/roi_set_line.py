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
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Monetary(string="Amount", currency_field='currency_id')
    qty = fields.Integer(string='Quantity')
    name = fields.Char(string='Name')
    sequence = fields.Integer(string="Sequence")
