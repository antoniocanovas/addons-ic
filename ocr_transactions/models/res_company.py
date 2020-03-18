# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api
import json
import shutil
import requests
from odoo.exceptions import ValidationError
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug('Can not `import queue_job`.')
    import functools


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_key = fields.Char(
        string='Api Key',
    )
    api_domain = fields.Char(
        default='http://biyectiva.com:5000',
        string='Api Url'
    )
    last_connection_date = fields.Date('Last connection date')
    ocr_transactions_jobs_ids = fields.Many2many(
        comodel_name='queue.job', column1='company_id', column2='job_id',
        string="Connector Jobs", copy=False,
    )

    @api.multi
    def get_header(self):
        api_key = self.env.user.company_id.api_key
        if api_key:
            header = {
                'X-API_KEY': api_key,
            }
            return header
        else:
            raise ValidationError(
                "You must set Api Key in company form.")

    @api.multi
    def get_documents_data(self, api_transaction_url, headers):
        response = requests.get(api_transaction_url, headers=headers)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            error = json.loads(response.content.decode('utf-8'))
            _logger.info(
                "Error from OCR server  %s" % error
            )

    @api.multi
    def create_queue_invoice_transactions(self, transactions_by_state):
        for i in range(len(transactions_by_state['FACTURAS'])):
            token = transactions_by_state['FACTURAS'][i]['token']
            exist = self.env['ocr.transactions'].search([("token", "=", token)])
            if exist.token:
                if exist.status == "downloaded":
                    print("CORRECTED")
                    invoice = self.env['account.invoice'].search([("ocr_transaction_id", "=", exist.id)])
                    print(invoice)
                    if invoice and invoice.state == 'draft':
                        invoice.unlink()
                        print("Borrada")
                    else:
                        exist.status = transactions_by_state['FACTURAS'][i]['status']
                else:
                    exist.status = transactions_by_state['FACTURAS'][i]['status']
            else:
                type_doc = transactions_by_state['FACTURAS'][i]['type']
                if transactions_by_state['FACTURAS'][i]['type'] == "emitida":
                    type_doc = "out_invoice"
                if transactions_by_state['FACTURAS'][i]['type'] == "recibida":
                    type_doc = "in_invoice"

                self.env['ocr.transactions'].create({
                    'status': transactions_by_state['FACTURAS'][i]['status'],
                    'type': type_doc,
                    'name': transactions_by_state['FACTURAS'][i]['client'],
                    'token': transactions_by_state['FACTURAS'][i]['token'],
                    'create_date': transactions_by_state['FACTURAS'][i]['created_at'],
                    'write_date': transactions_by_state['FACTURAS'][i]['updated_at'],
                })

    @api.multi
    def create_invoices(self, transactions_processed, api_transaction_url, header):
        for p in transactions_processed:
            api_transaction_url_token = "%s%s" % (api_transaction_url, p.token)
            p_invoice = self.get_documents_data(api_transaction_url_token, header)
            if p_invoice:
                for v in p_invoice["result"]["basic"].values():
                    self.env['ocr.values'].sudo().create({
                        'token': p.token,
                        'name': v["ERPName"],
                        'value': v["Value"]["Text"],
                        'ocr_transaction_id': p.id,
                    })
                    p.status = 'downloaded'

                partner_vat = self.env['ocr.values'].sudo().search([
                    ('ocr_transaction_id', '=', p.id), ('name', '=', 'CIF')])
                partner = self.env['res.partner'].search([("vat", "=", partner_vat.value)])
                if not partner:
                    account600_id = self.env['ir.model.data'].search([
                        ('name', '=', 'l10n_es.1_account_common_600'),
                        ('model', '=', 'account_tax')
                    ])
                    account600 = self.env['account.account'].search([('id', '=', account600_id.res_id)])

                    account700_id = self.env['ir.model.data'].search([
                        ('name', '=', 'l10n_es.1_account_common_700'),
                        ('model', '=', 'account_tax')
                    ])
                    account700 = self.env['account.account'].search([('id', '=', account700_id.res_id)])

                    partner = self.env['res.partner'].sudo().create({
                        'name': partner_vat.value,
                        'vat': partner_vat.value,
                        'ocr_sale_account_id': account600,
                        'ocr_purchase_account_id': account700,
                    })
                if partner:

                    date = self.env['ocr.values'].sudo().search([
                        ('ocr_transaction_id', '=', p.id),('name', '=', 'Fecha')])
                    if date.value:
                        invoice = self.env['account.invoice'].sudo().create({
                            'partner_id': partner.id,
                            'type': p.type,
                            'date_invoice': datetime.strptime(date.value, '%d/%m/%Y').date(),
                            'ocr_transaction_id': p.id
                        })
                    else:
                        invoice = self.env['account.invoice'].sudo().create({
                            'partner_id': partner.id,
                            'type': p.type,
                            'ocr_transaction_id': p.id
                        })
                if invoice:
                    self.get_attachment_data(p_invoice['image'], header)
                    attachment = self.generate_attachment(invoice, p)
                    body = "<p>created with OCR Documents</p>"
                    invoice.message_post(body=body, attachment_ids=[attachment.id])
                    invoice.message_main_attachment_id = [(4, attachment.id)]

    @api.multi
    def get_attachment_data(self, api_img_url, headers):
        response = requests.get(api_img_url, headers=headers, stream=True)

        if response.status_code == 200:
            with open('/tmp/test.jpg', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
        else:
            error = json.loads(response.content.decode('utf-8'))
            _logger.info(
                "Error from OCR server  %s" % error
            )

    @api.multi
    def generate_attachment(self, document, ocr_document):
        # podemos pasar res_model desde action_get_x para hacer geneérica esta función
        with open('/tmp/test.jpg', "rb") as pdf_file:
            pdf_file_encode = base64.b64encode(pdf_file.read())

        folder = self.env['documents.folder'].search([("id", "=", "2")])
        tag = self.env['documents.tag'].search([("name", "=", "To review")])
        tag_ids = [(4, tag.id)]
        return self.env['ir.attachment'].sudo().create({
            'name': ocr_document.name,
            'type': 'binary',
            'datas': pdf_file_encode,
            'datas_fname': ocr_document.name,
            'store_fname': ocr_document.name,
            'folder_id': folder.id,
            'tag_ids': tag_ids,
            'res_model': 'account.invoice',
            'res_id': document.id,
            'mimetype': 'image/jpg'
        })

    @api.multi
    def prepare_ocr_transactions(self):
        company = self.env.user.company_id

        queue_obj = self.env['queue.job'].sudo()
        new_delay = company.sudo().with_context(
            company_id=company.id
        ).with_delay().action_queue_get_invoices()
        job = queue_obj.search([
            ('uuid', '=', new_delay.uuid)
        ], limit=1)
        company.sudo().ocr_transactions_jobs_ids |= job

    @job
    @api.multi
    def action_queue_get_invoices(self):
        print("encolado")
        self.action_get_invoices()

    @api.multi
    def action_get_invoices(self):

        ########## Actualmente solo traemos facturas ###################
        api_transaction_url = "%s/facturas/" % self.env.user.company_id.api_domain
        header = self.get_header()

        transactions_by_state = self.get_documents_data(api_transaction_url, header)
        ############### Control status donwloaded #######################


        if transactions_by_state:
            self.create_queue_invoice_transactions(transactions_by_state)

        transactions_processed = self.env['ocr.transactions'].search([(
            "status", "=", 'processed'
        )], limit=1)
        if transactions_processed:
            self.create_invoices(transactions_processed, api_transaction_url, header)

        self.last_connection_date = datetime.now().date()
