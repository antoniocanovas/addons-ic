# Copyright

import base64

from odoo import fields, models, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class OcrTransactions(models.Model):
    _name = 'ocr.transactions'
    _description = 'Ocr Transactions'

    token = fields.Char('Api Token')
    state = fields.Char('Status')
    cleared = fields.Boolean('Cleared', default=False)
    type = fields.Char('Type')
    name = fields.Char('Customer')
    customer_vat = fields.Char('vat')
    value_ids = fields.One2many('ocr.values', 'ocr_transaction_id')
    ocr_upload_id = fields.Many2one('ocr.uploads')
    json_text = fields.Char('Json')
    attachment_id = fields.Many2one('ir.attachment', string='Invoice Document')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    next_token = fields.Char('Próxima Factura')
    previus_token = fields.Char('')
    transaction_error = fields.Char('Transaction Error Code')
    customer_api_key = fields.Char('Customer Api Key')

    token_list = fields.Char('Lista')

    @api.depends('invoice_id')
    def _get_invoice_reference(self):
        for record in self:
            print("DEBUG", record.invoice_id.ref)
            if record.invoice_id.ref:
                record.invoice_reference = record.invoice_id.ref
                #record.invoice_reference = record.invoice_id.ref
            else:
                record.invoice_reference = "None"

    invoice_reference = fields.Char('Referencia', compute=_get_invoice_reference)

    def show_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            try:
                form_view_id = self.env.ref("ocr_transactions.ocr_account_invoice_form").id
            except Exception as e:
                form_view_id = False
            return {
                'type': 'ir.actions.act_window',
                'name': 'action_ocr_in_invoice',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'views': [(form_view_id, 'form')],
                'target': 'current',
            }
        else:
            raise ValidationError("No hay Factura asociada")






