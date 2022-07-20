# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas <antonio.canovas@ingenieriacloud.com>
#    Pedro josé Baños Guirao <pedro@serincloud.com>
##############################################################################
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_expired_debt(self):
        for record in self:
            total = 0
            today = datetime.date.today()
            invoices = self.env['account.move'].search([('partner_id', '=', record.id),
                                                        ('state', '=', 'posted'),
                                                        ('payment_state', 'in', ['not_paid', 'partial']),
                                                        ('invoice_date_due', '<', today)])
            for r in invoices:
                total += r.amount_residual_signed
            record.expired_debt = total
    expired_debt = fields.Monetary(string='Expired debt', store=False, compute='_get_expired_debt')
