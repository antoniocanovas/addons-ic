# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
import json
import requests
from odoo.exceptions import ValidationError


import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug('Can not `import queue_job`.')
    import functools

TYPE = [
    ('emitida', 'Facturas emitidas'),
    ('recibida', 'Facturas de proveedor'),
]
STATE = [
    ('draft', 'Draft'),
    ('sending', 'Sending'),
    ('processing', 'Processing'),
    ('error', 'Error'),
    ('done', 'Done'),
]


class OcrUploads(models.Model):
    _name = 'ocr.uploads'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ocr Uploads'

    upload_transaction_error = fields.Char('upload Error Code')
    partner_id = fields.Many2one('res.partner')
    type = fields.Selection(
        selection=TYPE, string="Type", default='recibida',
    )
    state = fields.Selection(
        selection=STATE, string="Type", default='draft', track_visibility='onchange'
    )
    name = fields.Char('Name')
    ocr_transaction_ids = fields.One2many('ocr.transactions', 'ocr_upload_id')
    attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                relation="m2m_ocr_attachments_rel",
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Attachments")
    ocr_post_transactions_jobs_ids = fields.Many2many(
        comodel_name='queue.job', column1='upload_id', column2='job_id',
        string="Connector Jobs", copy=False,
    )


    @api.multi
    def get_uploader_header(self):
        api_key = self.env.user.company_id.api_key
        if api_key:
            header = {
                'Content-Type': 'application/json',
                'X-API_KEY': api_key,
            }
            return header
        else:
            raise ValidationError(
                "You must set Api Key in company form.")

    @api.multi
    def prepare_attachment(self, attachment, upload):
        self.ensure_one()

        strname = str(attachment.datas_fname)
        strlen = len(strname)

        ext = strname[(strlen - 3)] + strname[(strlen - 2)] + strname[(strlen - 1)]

        if ext == "JPG" or ext == "jpeg" or ext == "jpg":
            image = "data:image/jpeg;base64," + str(attachment.datas.decode('ascii'))
        elif ext == "pdf" or ext == "PDF":
            image = "data:application/pdf;base64," + str(attachment.datas.decode('ascii'))
        elif ext == "png" or ext == "PNG":
            image = "data:image/png;base64," + str(attachment.datas.decode('ascii'))
        elif ext == "iff" or ext == "tif" or ext == "TIF" or ext == "IFF":
            image = "data:image/tiff;base64," + str(attachment.datas.decode('ascii'))
        else:
            return False

        djson = {
            "type": upload.type,
            "image": image,
            "client": upload.partner_id.vat,
        }
        d_json = json.dumps(djson)
        return d_json

    @api.multi
    def create_ocr_transaction(self, token, attachment, upload):

        if upload.type == "emitida":
            type_doc = "out_invoice"
        if upload.type == "recibida":
            type_doc = "in_invoice"

        ocr_transaction_id = self.env['ocr.transactions'].create({
            'state': "Enviado",
            'ocr_upload_id': self.id,
            'type': type_doc,
            'name': upload.partner_id.vat,
            'token': token,
            'attachment_id': attachment.id ,
            #'create_date': transactions_by_state['created_at'],
        })
        return ocr_transaction_id

    @api.multi
    def prepare_ocr_post_transactions(self):

        if not self.partner_id.vat:
            raise ValidationError(
                "Partner has not vat defined")
        else:
            for upload in self:
                if upload.state == "processing" or upload.state == "sending":
                    raise ValidationError(
                        "Odoo is still uploading this!!! Please be patient")

                company = self.env.user.company_id

                jobs = self.env['queue.job'].sudo().search(["|",
                                                            ('state', '=', 'pending'), ('state', '=', 'enqueued')
                                                            ])
                eta = 20 + (len(jobs) * 20)

                queue_obj = self.env['queue.job'].sudo()
                new_delay = upload.sudo().with_context(
                    company_id=company.id
                ).with_delay(eta=eta).action_queue_post_invoices()
                job = queue_obj.search([
                    ('uuid', '=', new_delay.uuid)
                ], limit=1)
                upload.sudo().ocr_post_transactions_jobs_ids |= job
                upload.state = 'sending'

    @job
    @api.multi
    def action_queue_post_invoices(self):

        self.action_post_invoices()

    @api.multi
    def action_post_invoices(self):

        header = self.get_uploader_header()
        api_transaction_url = "%s/facturas/" % self.env.user.company_id.api_domain

        for attachment in self.attachment_ids:

            djson = self.prepare_attachment(attachment, self)
            if not djson:
                self.state = "error"
                self.upload_transaction_error = "No image to upload or invalid"
                _logger.info(
                    "Error from OCR server  image type not supported"
                )
            else:
                response = requests.post(api_transaction_url, headers=header, data=djson)

                if response.status_code == 200:
                    res = json.loads(response.content.decode('utf-8'))
                    ocr_transaction_id = self.create_ocr_transaction(res['token'], attachment, self)
                    self.ocr_transaction_ids = [(4, ocr_transaction_id.id)]
                else:
                    self.state = "error"
                    self.upload_transaction_error = json.loads(response.content.decode('utf-8'))
                    _logger.info(
                        "Error from OCR server  %s" % self.upload_transaction_error
                    )
        if self.state != "error":
            self.state = "sending"






