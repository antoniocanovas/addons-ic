

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
    ('sent', 'Sent'),
    ('cancelled', 'Cancelled'),
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

    @api.multi
    def post_correction_form(self):
        print("Correction FORM")

        url = http.request.env['ir.config_parameter'].get_param('web.base.url')
        print(url)
        url_portal = url + str("/invoice/correction")

        print(url_portal)


        #session = requests.session()
        #params = {'apikey': self.env.user.company_id.api_key}
        #response = session.post(url, params=params)


        return {'type': 'ir.actions.act_url',
                'url': '/invoice/correction',
                'target': 'current',
                'invoice': self,
                }

    @api.multi
    def prepare_invoice_send(self):

        for invoice in self:
            company = invoice.company_id
            #Set ETA
            jobs = self.env['queue.job'].sudo().search(["|",
                ('state', '=', 'pending'), ('state', '=', 'enqueued')
            ])
            eta = 30 + (len(jobs)*30)
            # Tomar VAT del usuario que envía a OCR y sea tipo Odoo
            pc = self.env['partner.credentials'].sudo().search([('partner_id.vat', '=', self.ocr_transaction_id.name)])
            if not pc:
                raise Warning((
                    "Revise que el cliente esté dado de alta en 'Partner Credentials' y configurados los campos de "
                    " 'Base de datos' y 'Servidor' en la pestaña SSO"
                ))
            else:

                queue_obj = self.env['queue.job'].sudo()
                new_delay = invoice.sudo().with_context(
                        company_id=company.id
                     ).with_delay(eta=eta).send_invoice(pc)
                job = queue_obj.search([
                    ('uuid', '=', new_delay.uuid)
                ], limit=1)
                invoice.sudo().ocr_invoice_jobs_ids |= job

    @job
    @api.multi
    def send_invoice(self, pc):
        self.ensure_one()
        self._send_invoice_to_remote(pc)

    @api.multi
    def _send_invoice_to_remote(self, pc):

        pc.set_parameters(self)




