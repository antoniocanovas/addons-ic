# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import timedelta


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    pnt_collaborator_id = fields.Many2one(
        comodel_name="res.partner",
        string='Collaborator',
        domain="[('is_company','=',1)]",
    )

    #@api.model
    #def create(self, vals):
    #    res = super(AccountInvoice, self).create(vals)
    #    return res

