# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
import json
from datetime import datetime
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
    #('emitida', 'Facturas emitidas'),
    ('recibida', 'Facturas de proveedor'),
    #('emitida_batch', 'Lote de facturas emitidas'),
    ('recibida_batch', 'Lote de facturas de proveedor'),
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
    partner_credentials_id = fields.Many2one('partner.credentials', string="Cliente", domain="[('type', '=', 'odoo')]")
    partner_id = fields.Many2one('res.partner', string="Cliente")
    type = fields.Selection(
        selection=TYPE, string="Type", default='recibida',
    )
    state = fields.Selection(
        selection=STATE, string="State", default='draft', track_visibility='onchange'
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
    ocr_delivery_upload = fields.Boolean(string='Es Gestor OCR',
                                   default=lambda self: self.env.user.company_id.ocr_delivery_company)
    invoice_origin_id = fields.Many2one('account.invoice')

    @api.constrains('attachment_ids')
    def _get_upload_name(self):
        for record in self:
            if record.type == "recibida_batch":
                tipo = "Lote de facturas recibidas"
            elif record.type == "emitida_batch":
                tipo = "Lote de facturas emitidas"
            elif record.type == "recibida":
                tipo = "recibida"
            elif record.type == "emitida":
                tipo = "emitida"

            #if not self.env.user.company_id.ocr_delivery_company:
            #    record.name = str(self.env.user.name) + " - " +\
            #                  str(datetime.utcnow().strftime('%d-%m-%Y')) + "-" + str(tipo)

    @api.multi
    def get_api_key(self):

        if self.partner_id == self.env.user.company_id.partner_id:
            api_key = self.env.user.company_id.api_key
        else:
            api_key = self.partner_credentials_id.client_api_key
        if not api_key:
            raise ValidationError(
                "You must set Api Key in company and/or credentials form.")
        else:
            return api_key

    @api.multi
    def get_uploader_header(self, api_key):
        header = {
            'Content-Type': 'application/json',
            'X-API_KEY': api_key,
        }
        return header

    @api.multi
    def prepare_attachment(self, attachment, upload):
        self.ensure_one()

        vat = upload.partner_id.get_ocr_vat()

        strname = str(attachment.datas_fname)
        strlen = len(strname)

        if attachment.datas:
            ext = strname[(strlen - 3)] + strname[(strlen - 2)] + strname[(strlen - 1)]
            if upload.type == 'emitida_batch' or upload.type == 'recibida_batch':
                if ext == "pdf" or ext == "PDF":
                    image = "data:application/pdf;base64," + str(attachment.datas.decode('ascii'))
                    djson = {
                        "type": upload.type,
                        "image": image,
                        # "client": upload.partner_id.vat,
                        "client": vat,
                    }
                    d_json = json.dumps(djson)
                    return d_json
                else:
                    raise ValidationError("El archivo de lotes debe ser PDF")
            else:
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
                    # "client": upload.partner_id.vat,
                    "client": vat,
                }
                d_json = json.dumps(djson)
                return d_json
        else:
            self.upload_transaction_error = str(self.upload_transaction_error) + \
                                            "No image to upload or invalid =>" + strname
            return False

    @api.multi
    def create_ocr_transaction(self, token, key, attachment, pre, nxt, upload, list, ):

        if upload.type == "emitida":
            type_doc = "out_invoice"
        if upload.type == "recibida":
            type_doc = "in_invoice"
        if upload.type == "emitida_batch":
            type_doc = "out_invoice"
        if upload.type == "recibida_batch":
            type_doc = "in_invoice"

        if self.invoice_origin_id:
            ocr_transaction_id = self.env['ocr.transactions'].create({
                'state': "Enviado",
                'ocr_upload_id': upload.id,
                'type': type_doc,
                'name': upload.partner_id.vat,
                'token': token,
                'customer_api_key': key,
                'attachment_id': attachment.id,
                'previus_token': pre,
                'next_token': nxt,
                'token_list': list,
                'invoice_id': self.invoice_origin_id.id
                #'create_date': transactions_by_state['created_at'],
            })
        else:
            if not self.invoice_origin_id:
                ocr_transaction_id = self.env['ocr.transactions'].create({
                    'state': "Enviado",
                    'ocr_upload_id': upload.id,
                    'type': type_doc,
                    'name': upload.partner_id.vat,
                    'token': token,
                    'customer_api_key': key,
                    'attachment_id': attachment.id,
                    'previus_token': pre,
                    'next_token': nxt,
                    'token_list': list,
                    # 'create_date': transactions_by_state['created_at'],
                })
        return ocr_transaction_id

    @api.multi
    def prepare_ocr_post_transactions(self):

        if self.env.user.company_id.ocr_delivery_company:
            if not self.partner_credentials_id:
                self.partner_id = self.env.user.company_id.partner_id.id
            else:
                self.partner_id = self.partner_credentials_id.partner_id.id
        else:
            self.partner_id = self.env.user.company_id.partner_id.id
        if not self.partner_id.vat:
            raise ValidationError("Partner has not vat defined")
        else:
            company = self.env.user.company_id
            if company.ocr_disable_queue_jobs:
                for upload in self:
                    if upload.state == "processing" or upload.state == "sending":
                        raise ValidationError(
                            "Odoo is still uploading this!!! Please be patient")
                    upload.action_post_invoices()
            else:
                for upload in self:
                    if upload.state == "processing" or upload.state == "sending":
                        raise ValidationError(
                            "Odoo is still uploading this!!! Please be patient")

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

    def prepare_ocr_post_transactions_from_invoice(self):

        if self.env.user.company_id.ocr_delivery_company:
            if not self.partner_credentials_id:
                self.partner_id = self.env.user.company_id.partner_id.id
            else:
                self.partner_id = self.partner_credentials_id.partner_id.id
        else:
            self.partner_id = self.env.user.company_id.partner_id.id
        if not self.partner_id.vat:
            raise ValidationError("Partner has not vat defined")
        else:
            company = self.env.user.company_id
            for upload in self:
                if upload.state == "processing" or upload.state == "sending":
                    raise ValidationError(
                        "Odoo is still uploading this!!! Please be patient")
                else:
                    upload.action_post_invoices()

    @job
    @api.multi
    def action_queue_post_invoices(self):

        self.action_post_invoices()

    @api.multi
    def action_post_invoices(self):

        api_transaction_url = "%s/facturas/" % self.env.user.company_id.api_domain
        api_key = self.get_api_key()
        header = self.get_uploader_header(api_key)

        for attachment in self.attachment_ids:
            print("FOR ATTACHMENT")
            djson = self.prepare_attachment(attachment, self)
            if not djson:
                self.state = "error"
                self.upload_transaction_error = str(self.upload_transaction_error) + \
                                                "Error from OCR server  image type not supported"
                _logger.info(
                    "Error from OCR server  image type not supported"
                )
            else:
                response = requests.post(api_transaction_url, headers=header, data=djson)
                if response.status_code == 200:
                    res = json.loads(response.content.decode('utf-8'))
                    # Ahora nos puede mandar una lista
                    if 'tokens' in res:
                        list = res['tokens']
                        for idx, token in enumerate(list):
                            if token != 'null':

                                if idx == 0 or list[idx - 1] == 'null':
                                    pre = 'null'
                                else:
                                    pre = list[(idx - 1) % len(list)]

                                if idx >= (len(list)-1) or (list[(idx + 1) % len(list)]) == 'null':
                                    nxt = 'null'
                                else:
                                    nxt = list[(idx + 1) % len(list)]

                                ocr_transaction_id = self.create_ocr_transaction(
                                    token, api_key, attachment, pre, nxt, self, list
                                )
                                self.ocr_transaction_ids = [(4, ocr_transaction_id.id)]
                            else:
                                self.upload_transaction_error = str(self.upload_transaction_error) + \
                                                                " Error " + \
                                                                str(attachment.datas_fname) + 'OCR post NULL'
                    else:
                        print("OCR_transaction")
                        ocr_transaction_id = self.create_ocr_transaction(
                            res['token'], api_key, attachment, False, False, self, False
                        )
                        self.ocr_transaction_ids = [(4, ocr_transaction_id.id)]
                else:
                    self.state = "error"
                    try:
                        res = json.loads(response.content.decode('utf-8'))
                        self.upload_transaction_error = str(self.upload_transaction_error) +\
                                                        " Error " +\
                                                        str(attachment.datas_fname) + str(res)
                    except Exception as e:
                        self.upload_transaction_error = str(self.upload_transaction_error) +\
                                                        " Error " + \
                                                        str(attachment.datas_fname)
                    _logger.info(
                        "Error from OCR server  %s" % self.upload_transaction_error
                    )
            if self.state != "error":
                self.state = "processing"







