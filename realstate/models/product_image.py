# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class ProductImage(models.Model):
    _inherit = 'product.image'

    property_id = fields.Many2one('realstate.property')




