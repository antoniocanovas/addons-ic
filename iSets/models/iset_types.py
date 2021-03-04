from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


TYPES = [
    ('project', 'Project'),
    ('repair', 'Repair'),
    ('production', 'Production'),
]


class IsetsTypes(models.Model):
    _name = 'iset.types'
    _description = 'iSet Types'

    name = fields.Char('Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    product_id = fields.Many2one('product.product', string='Product')

    type = fields.Selection(selection=TYPES, required=True, string='Types')
