from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    so_id = fields.Many2one(
        'sale.order',
        string="Obra",

    )
