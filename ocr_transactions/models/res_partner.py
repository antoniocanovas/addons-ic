from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

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

    def get_ocr_vat(self):
        for record in self:
            if record.vat:
                vat = record.vat.replace('-', '')
                vat = vat.replace('ES', '')
                vat = vat.replace('FR', '')
                vat = vat.replace('IT', '')
                vat = vat.replace('PR', '')
                vat.upper()
                return vat
            else:
                return False



