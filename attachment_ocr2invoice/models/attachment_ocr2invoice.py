# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api
import json
import shutil
import requests
import urllib.request
from PIL import Image


class Ocr2Invoice(models.Model):
    _name = 'ocr.invoice'
    _description = 'ocr2invoice'

    ocr_token = fields.Char('Api Token')
    ocr_datas = fields.Binary('Attachment')
    ocr_invoice_status = fields.Char('Status')
    ocr_invoice_type = fields.Char('Type')
    ocr_customer_name = fields.Char('Customer Name')
    ocr_date_created = fields.Char('Create date')
    ocr_date_updated = fields.Char('Updated at')

    ocr_values_id = fields.One2many('ocr.values', 'ocr_invoice_id')

  #  baseimponible0 = fields.Float('Base Imponible 0%')
  #  baseimponible4 = fields.Float('Base Imponible 4%')
  #  baseimponible10 = fields.Float('Base Imponible 10%')
  #  baseimponible21 = fields.Float('Base Imponible 21%')

  #  iva0 = fields.Float('IVA 0%')
   # iva4 = fields.Float('IVA 4%')
  #  iva10 = fields.Float('IVA 10%')
  #  iva21 = fields.Float('IVA 21%')

  #  tipoiva0 = fields.Float('IVA 0%')
  #  tipoiva4 = fields.Float('IVA 4%')
  #  tipoiva10 = fields.Float('IVA 10%')
   # tipoiva21 = fields.Float('IVA 21%')

  #  irpf2 = fields.Float('IRPF 2%')
   # irpf7 = fields.Float('IRPF 7%')
  #  irpf15 = fields.Float('IRPF 15%')
  #  irpf19 = fields.Float('IRPF 19%')

   # invoice_cif = fields.Char('CIF')
   # invoice_date = fields.Date('Invoice Date')
   # invoice_subtotal =fields.Float('Subtotal')
    #invoice_total = fields.Float('Total')
    #invoice_payment_method = fields.Char('Payment Method')

    @api.multi
    def get_invoice_data(self, api_invoice_url, headers):
        response = requests.get(api_invoice_url, headers=headers)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))

    def get_attachment_data(self, api_img_url, headers):
        response = requests.get(api_img_url, headers=headers, stream=True)

        if response.status_code == 200:
            with open('/tmp/test.jpg', 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return

    @api.multi
    def get_generate_attachment(self, invoice, ocr_document):

        with open('/tmp/test.jpg', "rb") as pdf_file:
            pdf_file_encode = base64.b64encode(pdf_file.read())

        folder = self.env['documents.folder'].search([("id", "=", "2")])
        tag = self.env['documents.tag'].search([("name", "=", "To review")])
        tag_ids = [(4, tag.id)]
        return self.env['ir.attachment'].sudo().create({
                'name': ocr_document.ocr_customer_name,
                'type': 'binary',
                'datas': pdf_file_encode,
                'datas_fname': ocr_document.ocr_customer_name,
                'store_fname': ocr_document.ocr_customer_name,
                'folder_id': folder.id,
                'tag_ids': tag_ids,
                'res_model': 'account.invoice',
                'res_id': invoice.id,
                'mimetype': 'image/jpg'
        })

    @api.multi
    def action_ocr2invoice_get(self):

        api_invoice_url = url = "%s/facturas/" % self.env.user.company_id.api_domain
        api_key = self.env.user.company_id.api_key

        print(api_invoice_url)
        print(api_key)

        headers = {
            'X-API_KEY': api_key,
        }

        invoices_by_state = self.get_invoice_data(api_invoice_url, headers)

        ############### CONTROL ERROR API KEY ###########################

        ############### Control status donwloaded #######################

        if invoices_by_state:
            for i in range(len(invoices_by_state['FACTURAS'])):
                token = invoices_by_state['FACTURAS'][i]['token']
                exist = self.env['ocr.invoice'].search([("ocr_token", "=", token)])
                if exist.ocr_token:
                    if exist.ocr_invoice_status != invoices_by_state['FACTURAS'][i]['status']:
                        exist.ocr_invoice_status = invoices_by_state['FACTURAS'][i]['status']
                else:
                    self.env['ocr.invoice'].create({
                        'ocr_invoice_status': invoices_by_state['FACTURAS'][i]['status'],
                        'ocr_invoice_type': invoices_by_state['FACTURAS'][i]['type'],
                        'ocr_customer_name': invoices_by_state['FACTURAS'][i]['client'],
                        'ocr_token': invoices_by_state['FACTURAS'][i]['token'],
                        'ocr_date_created': invoices_by_state['FACTURAS'][i]['created_at'],
                        'ocr_date_updated': invoices_by_state['FACTURAS'][i]['updated_at'],
                    })

        invoices_processed = self.env['ocr.invoice'].search([("ocr_invoice_status", "=", 'processed')], limit=1)
        if invoices_processed:
            for p in invoices_processed:
                api_invoice_url_token = "%s%s" % (api_invoice_url, p.ocr_token)
                p_invoice = self.get_invoice_data(api_invoice_url_token, headers)
                if p_invoice:
                    for v in p_invoice["result"]["basic"].values():
                        self.env['ocr.values'].sudo().create({
                            'token': p.ocr_token,
                            'name': v["ERPName"],
                            'value': v["Value"]["Text"],
                            'ocr_invoice_id': p.id,
                        })
                        p.ocr_invoice_status = 'downloaded'
                    print(p.ocr_customer_name)
                    partner = self.env['res.partner'].search([("name", "=", p.ocr_customer_name)])
                    if not partner:
                        partner_id = self.env['res.partner'].sudo().create({
                            'name': p.ocr_customer_name,
                        })
                        invoice = self.env['account.invoice'].sudo().create({
                                'partner_id': partner_id.id,
                            })
                    else:
                        print("Existe")
                        invoice = self.env['account.invoice'].sudo().create({
                          'partner_id': partner.id,
                        })
                    if invoice:
                        self.get_attachment_data(p_invoice['image'], headers)
                        attachment = self.get_generate_attachment(invoice, p)
                        body = "<p>created with OCR Documents</p>"
                        invoice.message_post(body=body, attachment_ids=[attachment.id])
                        invoice.message_main_attachment_id = [(4, attachment.id)]


                    #for v in range(len(p_invoice['result']['basic'])):
                    #    variables = list(p_invoice['result']['basic'])[v]
                    #    valor_key = p_invoice['result']['basic'][variables]['ERPName']
                    #    valor_key2 = p_invoice['result']['basic'][variables]['Text']
                    #    print(valor_key)
                    #    print(valor_key2)




                    #p.ocr_values_ids.token = p_invoice['result']['basic']['CIF']['Value']['Text']
                    #print(p.invoice_cif)

                    ###### GENERATE ATTACHMENT ###########
                    #self.get_attachment_data(p_invoice['image'], headers)
                    #with open('/tmp/test.jpg', "rb") as pdf_file:
                    #    pdf_file_encode = base64.b64encode(pdf_file.read())


                    #self.env['ir.attachment'].sudo().create({
                    #    'name': self.ocr_customer_name,
                    #    'type': 'binary',
                    #    'datas': pdf_file_encode,
                    #    'datas_fname': self.ocr_customer_name,
                    #    'store_fname': self.ocr_customer_name,
                    #    'res_model': 'ocr.invoice',
                    #    'res_id': self.id,
                    #    'mimetype': 'image/jpg'
                    #})



