from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    ocr_transaction_id = fields.Many2one('ocr.transactions', string='OCR', readonly=True)
    customer_id = fields.Many2one('res.partner', readonly=True, string='Customer')

    @api.constrains('ocr_transaction_id')
    def check_customer_id(self):
        for record in self:
            if record.ocr_transaction_id:
                record.customer_id = record.ocr_transaction_id.ocr_upload_id.partner_id.id


