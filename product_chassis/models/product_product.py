# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    SERINCLOUD, S.L.
##############################################################################
from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends('product_tmpl_id.chassis_pt')
    def get_chassis_pp(self):
        for record in self:
            record['chassis_pp'] = record.product_tmpl_id.chassis_pt
    chassis_pp = fields.Char(
        string='Chassis', store=True, compute=get_chassis_pp, readonly=False,
        help='Vehicle or accessory chassis code for variants.'
    )
