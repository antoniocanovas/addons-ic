

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo import fields, models, api
import requests
from odoo import http
import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug('Can not `import queue_job`.')
    import functools

REMOTE_STATES = [
    ('not_sent', 'Not sent'),
    ('sending', 'Sending'),
    ('sent', 'Sent'),
    ('error', 'Error'),
    ('cancelled', 'Cancelled'),
]

REMOTE_TYPES = [
    ('in_invoice', 'Facturas Proveedor'),
    ('in_refund', 'Rectificativa Proveedor'),
]


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    ocr_invoice_jobs_ids = fields.Many2many(
        comodel_name='queue.job', column1='invoice_id', column2='job_id',
        string="Connector Jobs", copy=False,
    )
    remote_send_failed = fields.Boolean("Send Status")
    remote_state = fields.Selection(
        selection=REMOTE_STATES, string="Remote state", default='not_sent',
        readonly=True, copy=False,
        help="Mark as sent when succesfully created on remote client",
    )
    remote_type = fields.Selection(
        selection=REMOTE_TYPES, string="Tipo", default='in_invoice',
        help="Mark as refund to create a refund invoice in customer Odoo",
    )
    invoice_sync_error = fields.Char('Error')
    to_correct = fields.Boolean("For correction portal", default=False)

    @api.constrains('ocr_transaction_id')
    def check_customer_id(self):
        for invoice in self:
            if invoice.ocr_transaction_id:
                #pc = self.env['partner.credentials'].sudo().search([
                #    ('partner_id.vat', '=', self.ocr_transaction_id.name)], limit=1)
                pc = self.env['partner.credentials'].sudo().search([
                        ('client_api_key', '=', self.ocr_transaction_id.customer_api_key)], limit=1)
                if pc:
                    invoice.customer_id = pc.partner_id.id
                # invoice.customer_id = invoice.ocr_transaction_id.ocr_upload_id.partner_id.id

    @api.multi
    def prepare_invoice_send(self):

        for invoice in self:
            if invoice.amount_total < 0:
                raise Warning((
                    "La factura tiene TOTAL negativo, por favor revise la factura"
                ))
            company = invoice.company_id
            #Set ETA
            jobs = self.env['queue.job'].sudo().search(["|",
                ('state', '=', 'pending'), ('state', '=', 'enqueued')
            ])
            eta = 20 + (len(jobs)*20)
            #Tomar VAT del usuario que envía a OCR y sea tipo Odoo
            pc = self.env['partner.credentials'].sudo().search([
                ('client_api_key', '=', self.ocr_transaction_id.customer_api_key),
                ('type', '=', 'odoo'),
            ])[0]

            if len(invoice.partner_id.vat) < 11:
                raise Warning((
                                  "El CIF de proveedor no está en formato VIES"
                ))
            if not pc.url or not pc.db or not pc.remote_company_id:
                raise Warning((
                                  "Revise los datos de Credencial, falta Url Base de datos o Id de empresa"
                ))
            if pc.url[-1] == '/':
                raise Warning((
                                  "La Url de Credencial no puede acabar en '/'"
                ))
            if len(pc) > 1:
                raise Warning((
                    "Hay dos Partner Credentials con mismo VAT o Número de documento de identificación"
                ))
            else:
                if not pc:
                    raise Warning((
                        "Revise que el cliente esté dado de alta en 'Partner Credentials' y configurados los campos de "
                        " 'Base de datos' y 'Servidor' en la pestaña SSO"
                    ))
                if not invoice.invoice_line_ids:
                    raise Warning((
                        "La factura no contiene líneas de factura"
                    ))
                else:
                    queue_obj = self.env['queue.job'].sudo()
                    new_delay = invoice.sudo().with_context(
                            company_id=company.id
                         ).with_delay(eta=eta).send_invoice(pc)
                    job = queue_obj.search([
                        ('uuid', '=', new_delay.uuid)
                    ], limit=1)
                    invoice.remote_state = 'sending'
                    invoice.sudo().ocr_invoice_jobs_ids |= job

    @job
    @api.multi
    def send_invoice(self, pc):
        self.ensure_one()
        self._send_invoice_to_remote(pc)

    @api.multi
    def _send_invoice_to_remote(self, pc):
        pc.set_parameters(self)




