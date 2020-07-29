# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from datetime import datetime, timedelta
import json
from random import randint
import requests
from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
        default='https://ocr.biyectiva.com:6000',
        string='Api Url'
    )
    last_connection_date = fields.Date('Last connection date')
    #last_connection_date_char = fields.Char('Last connection')
    ocr_transactions_jobs_ids = fields.Many2many(
        comodel_name='queue.job', column1='company_id', column2='job_id',
        string="Connector Jobs", copy=False,
    )
    ocr_delivery_company = fields.Boolean('Gestiona OCR de clientes', default=False)
    ocr_disable_queue_jobs = fields.Boolean('Avoid queue_job', default=False)

    @api.multi
    def create_apikey_list(self):
        ApiKeys = []
        if self.ocr_delivery_company:
            ocr_clients = self.env['partner.credentials'].sudo().search([])
            for client in ocr_clients:
                if client.client_api_key:
                    ApiKeys.append(client.client_api_key)
        if self.env.user.company_id.api_key:
            ApiKeys.append(self.env.user.company_id.api_key)
        if len(ApiKeys) > 0:
            return ApiKeys
        else:
            raise ValidationError(
                "You must set Api Key in company and/or credentials form.")

    @api.multi
    def get_header(self, api_key):
        if api_key:
            header = {
                'X-API_KEY': api_key,
            }
            return header

    @api.multi
    def random_with_N_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)


    @api.multi
    def clean_vat(self, vat):
        vat_cleaned = vat.replace('-', '')
        vat_cleaned = vat_cleaned.replace(" ", "")
        vat_cleaned = vat_cleaned.replace('ES', '')
        vat_cleaned = vat_cleaned.replace('FR', '')
        vat_cleaned = vat_cleaned.replace('IT', '')
        vat_cleaned = vat_cleaned.replace('PR', '')
        vat_cleaned.upper()
        return vat_cleaned

    @api.multi
    def get_partner_by_vat(self, vat):
        vat_cleaned = self.clean_vat(vat.value)

        partner = self.env['res.partner'].search(["|",
                                                  ("vat", "=", vat.value),
                                                  ("vat", "=", vat_cleaned),
                                                  ], limit=1)

        if partner:
            return partner
        else:

            partners = self.env['res.partner'].search([])
            for p in partners:
                if p.vat != False:
                    p_vat = self.clean_vat(p.vat)
                    if p_vat == vat_cleaned:
                        return p
            return False

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
    def create_queue_invoice_transactions(self, transactions_by_state, key):
        #### Comprobar si hay que crearlo, actualizarlo o ignorarlo ####
        for i in range(len(transactions_by_state['FACTURAS'])):
            token = transactions_by_state['FACTURAS'][i]['token']
            #client = transactions_by_state['FACTURAS'][i]['client']
            exist = self.env['ocr.transactions'].search([
                ("token", "=", token),
            ], limit=1)
            # No se Borran facturas, solo actualizamos el transaction si no hay líneas de factura
            # Si hay lineas no debe actualizar estado
            if exist.token:
                print("Lee Facturas y actualiza estado")
                if exist.state != transactions_by_state['FACTURAS'][i]['status']:
                    exist.state = transactions_by_state['FACTURAS'][i]['status']
            else:
                print("Lee Facturas y crea transaction")
                type_doc = transactions_by_state['FACTURAS'][i]['type']
                if transactions_by_state['FACTURAS'][i]['type'] == "emitida":
                    type_doc = "out_invoice"
                if transactions_by_state['FACTURAS'][i]['type'] == "recibida":
                    type_doc = "in_invoice"

                self.env['ocr.transactions'].create({
                    'state': transactions_by_state['FACTURAS'][i]['status'],
                    'type': type_doc,
                    'name': transactions_by_state['FACTURAS'][i]['client'],
                    'token': transactions_by_state['FACTURAS'][i]['token'],
                    'customer_api_key': key,
                    'next_token': False,
                    'previus_token': False,
                    'create_date': transactions_by_state['FACTURAS'][i]['created_at'],
                    'write_date': transactions_by_state['FACTURAS'][i]['updated_at'],
                })

    @api.multi
    def update_transactions_error_code(self, transactions_with_errors, api_transaction_url, header):
        for t in transactions_with_errors:
            api_transaction_url_token = "%s%s" % (api_transaction_url, t.token)
            ocr_document_data = self.get_documents_data(api_transaction_url_token, header)
            t.json_text = ocr_document_data
            if ocr_document_data:
                if ocr_document_data["result"]["status"] == "ERROR":
                    t.transaction_error = ocr_document_data["result"]["reason"]
                    t.state = 'downloaded'

    @api.multi
    def ocr_update_values(self, t, ocr_document_data, type_values):
        for v in ocr_document_data["result"][type_values].values():
            ocr_values = self.env['ocr.values'].sudo().search([
                ('token', '=', t.token),
                ('name', '=', v["ERPName"])])
            for ocrv in ocr_values:
                ocrv.value = v["Value"]["Text"]
            if not ocr_values:
                self.env['ocr.values'].sudo().create({
                    'token': t.token,
                    'name': v["ERPName"],
                    'value': v["Value"]["Text"],
                    'ocr_transaction_id': t.id,
                })
        t.state = 'downloaded'

    @api.multi
    def create_invoices(self, transactions_processed, api_transaction_url, header):
        for t in transactions_processed:
            print("Por transaction procesed")
            invoice = self.env['account.invoice'].sudo().search([
                ("ocr_transaction_id.token", "=", t.token),
            ], limit=1)
            print("invoice",invoice)
            previus_ocr_values = self.env['ocr.values'].sudo().search([
                ("ocr_transaction_id", "=", t.id)
            ])
            print("VALUES",previus_ocr_values)

            api_transaction_url_token = "%s%s" % (api_transaction_url, t.token)
            ocr_document_data = self.get_documents_data(api_transaction_url_token, header)
            t.json_text = ocr_document_data

            if not ocr_document_data:
                print("No ha devuelto datos")
                t.json_text = "Sin datos del servidor"
                t.state = 'error'
            else:
                print("Hay datos")
                if invoice:
                    print("Hay factura")
                    if not invoice.invoice_line_ids:
                        print("Sin lineas")
                        basic_values = self.ocr_update_values(t, ocr_document_data, "basic")
                        extended_values = self.ocr_update_values(t, ocr_document_data, "extended")
                        t.state = 'downloaded'
                    else:
                        print("Con lineas")
                        t.state = 'downloaded'

                elif not previus_ocr_values:
                    print("No hay factura ni valores previos")
                    for v in ocr_document_data["result"]["basic"].values():
                        self.env['ocr.values'].sudo().create({
                            'token': t.token,
                            'name': v["ERPName"],
                            'value': v["Value"]["Text"],
                            'ocr_transaction_id': t.id,
                        })
                    for v in ocr_document_data["result"]["extended"].values():
                        self.env['ocr.values'].sudo().create({
                            'token': t.token,
                            'name': v["ERPName"],
                            'value': v["Value"]["Text"],
                            'ocr_transaction_id': t.id,
                        })
                    if ocr_document_data["result"]["status"] == "ERROR":
                        t.transaction_error = ocr_document_data["result"]["reason"]
                    t.state = 'downloaded'

                    partner_vat = self.env['ocr.values'].sudo().search([
                        ('token', '=', t.token), ('name', '=', 'CIF')], limit=1)

                    if partner_vat:
                        partner = self.get_partner_by_vat(partner_vat)
                        partner_name_value = partner_vat.value
                    else:
                        partner = False
                        partner_name_value = self.random_with_N_digits(8)
                        partner_name_value = str(partner_name_value)+"Z"
                    if not partner:
                        account600_id = self.env['ir.model.data'].search([
                            ('name', '=', '1_account_common_600'),
                            ('model', '=', 'account.account')
                        ])
                        account600 = self.env['account.account'].search([('id', '=', account600_id.res_id)])
                        account700_id = self.env['ir.model.data'].search([
                            ('name', '=', '1_account_common_7000'),
                            ('model', '=', 'account.account')
                        ])
                        account700 = self.env['account.account'].search([('id', '=', account700_id.res_id)])

                        partner = self.env['res.partner'].sudo().create({
                            'name': str(partner_name_value),
                            'vat': str(partner_name_value),
                            'company_type': 'company',
                            'ocr_sale_account_id': account700.id,
                            'ocr_purchase_account_id': account600.id,
                        })
                    if partner:
                        date = self.env['ocr.values'].sudo().search([
                            ('token', '=', t.token), ('name', '=', 'Fecha')], limit=1)

                        if date.value:
                            date_invoice = datetime.strptime(date.value, '%d/%m/%Y').date()
                        else:
                            date_invoice = False

                        reference = self.env['ocr.values'].sudo().search([
                            ('token', '=', t.token), ('name', '=', 'NumFactura')], limit=1)

                        if not reference:
                            reference_value = False
                        else:
                            reference_value = reference.value

                        if t.type == 'in_invoice':
                            invoice = self.env['account.invoice'].sudo().create({
                                'partner_id': partner.id,
                                'type': t.type,
                                'reference': reference_value,
                                'date_invoice': date_invoice,
                                'ocr_transaction_id': t.id,
                                'is_ocr': True,
                            })
                        else:
                            invoice = self.env['account.invoice'].sudo().create({
                                'partner_id': partner.id,
                                'type': t.type,
                                'date_invoice': date_invoice,
                                'ocr_transaction_id': t.id,
                                'is_ocr': True,
                            })

                    if invoice:
                        t.invoice_id = invoice.id
                        attachment = self.generate_attachment(ocr_document_data['image'], header, invoice, t)
                        body = "<p>created with OCR Documents</p>"
                        if attachment:
                            invoice.message_post(body=body, attachment_ids=[attachment.id])
                            invoice.message_main_attachment_id = [(4, attachment.id)]

    @api.multi
    def generate_attachment(self, api_img_url, headers, document, ocr_document):
        response = requests.get(api_img_url, headers=headers, stream=True)
        if response.status_code == 200:

            img_file_encode = base64.b64encode(response.content)

            return self.env['ir.attachment'].sudo().create({
                    'name': str(ocr_document.name) + "_" + str(ocr_document.id),
                    'type': 'binary',
                    'datas': img_file_encode,
                    'datas_fname': str(ocr_document.name) + "_" + str(ocr_document.id),
                    'store_fname': str(ocr_document.name) + "_" + str(ocr_document.id),
                    'res_model': 'account.invoice',
                    'res_id': document.id,
                    'mimetype': 'image/jpeg'
                })

        else:
            ocr_document.transaction_error = json.loads(response.content.decode('utf-8'))
            _logger.info(
                "Error from OCR server  %s" % ocr_document.transaction_error
            )

    @api.multi
    def mark_uploads_done(self, transactions_processed):
        for t in transactions_processed:
            if t.ocr_upload_id:
                if t.ocr_upload_id.state != "done":
                    f_state = "done"
                    for transaction in t.ocr_upload_id.ocr_transaction_ids:
                        if transaction.state == "error":
                            f_state = "error"
                        elif transaction.state == "processing" or transaction.state == "sending":
                            f_state = "processing"

                    t.ocr_upload_id.state = f_state

    @api.multi
    def check_dbcopy_instance(self):
        company = self.env.user.company_id

        if company.master_db_name != self.env.cr.dbname:
            cron_job = self.env['ir.cron'].sudo().search([('name', '=', '=> OCR transactions GET')])
            if cron_job:
                cron_job.active = False
            jobs_started = self.env['queue.job'].sudo().search([
                                                        ('state', '=', 'started'),
                                                        ])
            for job in jobs_started:
                job.unlink()
            jobs = self.env['queue.job'].sudo().search(["|",
                                                        ('state', '=', 'pending'),
                                                        ('state', '=', 'enqueued'),
                                                        ])
            for job in jobs:
                job.state = 'done'

    @api.multi
    def prepare_ocr_get_transactions(self):
        company = self.env.user.company_id

        if company.ocr_disable_queue_jobs:
            company.action_get_invoices()
        else:
            jobs = self.env['queue.job'].sudo().search(["|",
                                                        ('state', '=', 'pending'), ('state', '=', 'enqueued')
                                                        ])
            eta = 20 + (len(jobs) * 20)

            queue_obj = self.env['queue.job'].sudo()
            new_delay = company.sudo().with_context(
                company_id=company.id
            ).with_delay(eta=eta).action_queue_get_invoices()
            job = queue_obj.search([
                ('uuid', '=', new_delay.uuid)
            ], limit=1)
            company.sudo().ocr_transactions_jobs_ids |= job

    @job
    @api.multi
    def action_queue_get_invoices(self):

        self.action_get_invoices()

    @api.multi
    def action_get_invoices(self):
        ########## Comprobamos si somos OCR Manager ####################
        ApiKeys = self.create_apikey_list()
        ########## Actualmente solo traemos facturas ###################
        api_transaction_url = "%s/facturas/" % self.env.user.company_id.api_domain
        ########## Hacemos una consulta por cada ApiKey ################
        for key in ApiKeys:
            header = self.get_header(key)

            transactions_by_state = self.get_documents_data(api_transaction_url, header)
            ############### Control status donwloaded #######################
            if transactions_by_state:
                self.create_queue_invoice_transactions(transactions_by_state, key)

            transactions_processed = self.env['ocr.transactions'].search([
                                                                            ("state", "=", 'processed'),
                                                                            ("customer_api_key", "=", key),
                                                                        ], limit=30)
            transactions_with_errors = self.env['ocr.transactions'].search([
                                                                        ("state", "=", 'error'),
                                                                        ("customer_api_key", "=", key),
                                                                          ], limit=10)
            if transactions_with_errors:
                self.update_transactions_error_code(transactions_with_errors, api_transaction_url, header)

            if transactions_processed:
                self.create_invoices(transactions_processed, api_transaction_url, header)
                self.mark_uploads_done(transactions_processed)

            time = datetime.now()
            self.last_connection_date = time.strftime('%Y-%m-%d %H:%M:%S')

    @api.multi
    def ocr_delete_old_transactions(self):
        transactions = self.env['ocr.transactions'].sudo().search([])
        ## DOMAIN : '|', ("state", "=", 'downloaded'), ("state", "=", 'error')
        for transaction in transactions:
            if (datetime.utcnow() - transaction.write_date) > timedelta(days=25):
                transaction.sudo().unlink()

    @api.multi
    def ocr_restart_halted_queue_jobs(self):
        jobs = self.env['queue.job'].sudo().search(["|",
                                                    ('state', '=', 'started'), ('state', '=', 'enqueued')
                                                    ])
        print("Ejecución")
        for job in jobs:
            print("Encontrados", jobs)
            desired_eta = datetime.now() + timedelta(seconds=200)

            if (datetime.utcnow() - job.date_created) > timedelta(minutes=30):
                job.state = 'pending'

    @api.multi
    def ocr_mark_invoice_as_ocr(self):
        invoices = self.env['account.invoice'].sudo().search([('type', '=', 'in_invoice')])
        for invoice in invoices:
            invoice.is_ocr = True




