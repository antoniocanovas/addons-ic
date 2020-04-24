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

    #@api.onchange('write_date')
    #def get_uppercase_vat(self):
    #    if self.vat:
    #        self.vat = str(self.vat).upper()


