from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def send_through(self):

        print(self.message_main_attachment_id)
        print(self.message_main_attachment_id.name)



        ocr_upload = self.env['ocr.uploads'].create({
            'name': str(self.env.user.name) + " - " +\
                              str(datetime.utcnow().strftime('%d-%m-%Y')) ,
            'type': 'recibida',
            'attachment_ids': [(6,0,[self.message_main_attachment_id.id])],
            'invoice_origin_id': self.id,
        })
        if ocr_upload:

            ocr_upload.prepare_ocr_post_transactions()
            self.ocr_transaction_id = ocr_upload.ocr_transaction_ids[0]

        #raise ValidationError("Print DEBUG")



