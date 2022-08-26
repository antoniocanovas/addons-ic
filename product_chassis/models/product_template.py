# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends('attribute_line_ids')
    def get_chassis_pt(self):
        for record in self:
            record['chassis_pt'] = ""
    chassis_pt = fields.Char(
        string='Chassis', store=True, compute=get_chassis_pt, readonly=False,
        help='Vehicle or accessory chassis code.'
    )
