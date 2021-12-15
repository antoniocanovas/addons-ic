# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas <antonio.canovas@ingenieriacloud.com>
#    Pedro josé Baños Guirao <pedro@serincloud.com>
##############################################################################
from odoo import api, fields, models, _


class ResPartnerDeafultJournal(models.Model):
    _inherit = 'res.partner'

    journal_sale_id = fields.Many2one(
        'account.journal',
        string='Sale Journal',
        domain=[('type', '=', 'sale')]
    )
    journal_purchase_id = fields.Many2one(
        'account.journal',
        string='Purchase Journal',
        domain=[('type', '=', 'purchase')]
    )
