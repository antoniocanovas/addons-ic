# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class OcrTransactions(models.Model):
    _name = 'ocr.transactions'
    _description = 'Ocr Transactions'

    ocr_token = fields.Char('Api Token')
    ocr_transaction_status = fields.Char('Status')
    ocr_document_type = fields.Char('Type')
    ocr_customer_name = fields.Char('Customer')
    ocr_date_created = fields.Char('Create date')
    ocr_date_updated = fields.Char('Updated at')
    ocr_document_cif = fields.Char('Customer')      # Sin uso en esta versión
    ocr_value_ids = fields.One2many('ocr.values', 'ocr_transaction_id')






