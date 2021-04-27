from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    repair_id = fields.Many2one(
        'repair.order',
        string="Reparaciones",
        domain="[('state','in',['confirmed','under_repair','ready'])]"
    )
