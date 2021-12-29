from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductLeadRel(models.Model):
    _name = 'product.lead.rel'
    _description = 'Relational table for prodcut and opportunities'

    product_id = fields.Many2one('product.template', string='Product')
    lead_id = fields.Many2one('crm.lead', string="Oportunity")

