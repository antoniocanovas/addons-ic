# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class OcrTransactions(models.Model):
    _name = 'ocr.transactions'
    _description = 'Ocr Transactions'

    token = fields.Char('Api Token')
    state = fields.Char('Status')
    type = fields.Char('Type')
    name = fields.Char('Customer')
    value_ids = fields.One2many('ocr.values', 'ocr_transaction_id')
    ocr_upload_id = fields.Many2one('ocr.uploads')
    json_text = fields.Char('Json')
    attachment_id = fields.Many2one('ir.attachment', string='Invoice Document')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')






