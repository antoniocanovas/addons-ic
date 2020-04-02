from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ocr_sale_account_id = fields.Many2one(
        'account.account',
    )
    ocr_purchase_account_id = fields.Many2one(
        'account.account',
    )
    ocr_sale_product_id = fields.Many2one(
        'product.product',
    )
    ocr_purchase_product_id = fields.Many2one(
        'product.product',
    )

