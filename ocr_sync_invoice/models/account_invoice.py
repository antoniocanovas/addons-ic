
import xmlrpc.client
from datetime import datetime
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug('Can not `import queue_job`.')
    import functools

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    ocr_invoice_jobs_ids = fields.Many2many(
        comodel_name='queue.job', column1='invoice_id', column2='job_id',
        string="Connector Jobs", copy=False,
    )
    remote_send_failed = fields.Boolean("Send Status")

    @api.multi
    def prepare_invoice_send(self):
        print("Entra")
        queue_obj = self.env['queue.job'].sudo()
        for invoice in self:
            company = invoice.company_id
            #Set ETA
            #eta = company._get_sii_eta()
            #new_delay = invoice.sudo().with_context(
            #    company_id=company.id
            #).with_delay(
            #    eta=eta if not invoice.sii_send_failed else False,
            #).confirm_one_invoice()

            #Tomar VAT del usuario que envía a OCR y sea tipo Odoo
            pc = self.env['partner.credentials'].sudo().search([('partner_id.vat', '=', self.ocr_transaction_id.name)])
            print(pc.partner_id.vat)
            if not pc:
                raise Warning((
                    "Revise que el cliente esté dado de alta en 'Partner Credentials' y configurados los campos de "
                    " 'Base de datos' y 'Servidor' en la pestaña SSO"
                ))
            else:
                new_delay = invoice.sudo().with_context(
                        company_id=company.id
                     ).with_delay().send_invoice(pc)
                job = queue_obj.search([
                    ('uuid', '=', new_delay.uuid)
                ], limit=1)
                invoice.sudo().ocr_invoice_jobs_ids |= job
                self.send_invoice(pc)

    @api.multi
    def check_partner_in_remote(self, partner, conn, pc):
        partner_exist = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'],
                                               'res.partner', 'search_read',
                                               [[('vat', '=', partner.vat)]],
                                               {'fields': ['id'], 'limit': 1})
        if not partner_exist:
            try:
                partner_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'], 'res.partner', 'create',
                                                   [{
                                                       'name': partner.name,
                                                       'vat': partner.vat,

                                                   }])

                return partner_id
            except Exception as e:
                raise Warning(("Exception when calling remote server $CreatePartner: %s\n" % e))
        return partner_exist[0]['id']


    @api.multi
    def write_invoice_to_remote(self, invoice, conn, pc):
        print("check")

        partner_id = self.check_partner_in_remote(invoice.partner_id, conn, pc)

        try:
            exist = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'],
                                              'ir.model.data', 'search',
                                              [[('model', '=', 'account.invoice'),
                                                ('name', '=',
                                                 str(pc.remote_company_id) + '_account_invoice_' + str(invoice.id))
                                                ]],
                                              {'limit': 1})

        except Exception as e:
            raise Warning(("Exception when calling remote server $CreateInvoice: %s\n" % e))
        print(invoice)
        print(invoice.partner_id.id)
        print(invoice.type)
        if len(exist) == 0:
            print("Cretae")
            try:
                invoice_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'], 'account.invoice', 'create',
                                                       [{
                                                           'partner_id': partner_id,
                                                           'type': invoice.type,
                                                           'date_invoice': invoice.date_invoice

                                                       }])
            except Exception as e:
                raise Warning(("Exception when calling remote server $RegisterInvoice: %s\n" % e))

            if invoice_id:
                print("register")
                try:
                    external_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'], 'ir.model.data',
                                                            'create', [{
                            'module': 'ase_replication_server',
                            'model': 'account.invoice',
                            'name': str(pc.remote_company_id) + '_account_invoice_' + str(invoice.id),
                            'res_id': invoice_id,
                        }])

                    return invoice_id
                except Exception as e:
                    raise Warning(("Exception when calling remote server $Invoice: %s\n" % e))
            else:
                raise Warning(("Error inesperado, por favor inténtelo de nuevo más tarde"))


    @job
    @api.multi
    def send_invoice(self, pc):
        self._send_invoice_to_remote(pc)

    @api.multi
    def _send_invoice_to_remote(self, pc):
        print("sending")

        conn = pc.setxmlrpc()
        company = pc.set_remote_company(conn)

        for invoice in self:
            remote_id = self.write_invoice_to_remote(invoice, conn, pc)


