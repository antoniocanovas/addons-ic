# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PosProductTemplate(models.Model):
    _inherit = 'product.template'

    is_addon = fields.Boolean(string='Is Addon',default=False)
    has_addons = fields.Boolean(string='Has Addons',default=False)
    addon_price_hidden = fields.Boolean(string='Addon Price Hidden',default=False)

class PosOrderLineGroup(models.Model):
    _inherit = 'pos.order.line'

    line_stamp = fields.Char(string='Line Stamp')



    
