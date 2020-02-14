from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    ocr_transaction_id = fields.Many2one('ocr.transactions', string='OCR')
