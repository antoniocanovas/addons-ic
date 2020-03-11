
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
            if not pc:
                raise Warning((
                    "Revise que el cliente esté dado de alta en 'Partner Credentials' y configurados los campos de "
                    " 'Base de datos' y 'Servidor' en la pestaña SSO"
                ))
            else:

                queue_obj = self.env['queue.job'].sudo()
                new_delay = invoice.sudo().with_context(
                        company_id=company.id
                     ).with_delay().send_invoice(pc)
                job = queue_obj.search([
                    ('uuid', '=', new_delay.uuid)
                ], limit=1)
                invoice.sudo().ocr_invoice_jobs_ids |= job

  #  @api.multi
  #  def check_partner_in_remote(self, partner, conn, pc):
  #      partner_exist = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'],
  #                                             'res.partner', 'search_read',
  #                                             [[('vat', '=', partner.vat)]],
  #                                             {'fields': ['id'], 'limit': 1})
  #      if not partner_exist:
  #          try:
  #              partner_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'], 'res.partner', 'create',
  #                                                 [{
  ##                                                     'name': partner.name,
 #                                                      'vat': partner.vat,
#
#                                                   }])
#
#                return partner_id
#            except Exception as e:
#                raise Warning(("Exception when calling remote server $CreatePartner: %s\n" % e))
#        return partner_exist[0]['id']

#    @api.multi
#    def get_lines(self, conn, pc):
#        invoice_line_list = []
#        line_dic = {}
#        for line in self.invoice_line_ids:
#            if line.product_id:
#                product_id = self.get_product(line.product_id, conn, pc)
#                print("DEBUG2")
#                print(product_id)
#            if line.account_id:
#                account_id = pc.get_account(line.account_id, conn)
#            if line.asset_profile_id:
#                profile_id = pc.get_profile_asset(line.asset_profile_id, conn)
#            if line.invoice_line_tax_ids:
#                tax_ids = pc.get_taxes(line.invoice_line_tax_ids, conn)
#
#            line_dic = {
#                        'product_id': product_id,
#                        'account_id': account_id,
#                        'profile_id': profile_id,
#                        'tax_ids': tax_ids,
#                      }
#
        #    invoice_line_list.append(line_dic)
        #return invoice_line_list

#    @api.multi
#    def write_invoice_to_remote(self, conn, pc):
#
#        partner_id = self.check_partner_in_remote(self.partner_id, conn, pc)
#
#        try:
#            exist = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'],
#                                              'ir.model.data', 'search',
#                                              [[('model', '=', 'account.invoice'),
#                                                ('name', '=',
#                                                 str(pc.remote_company_id) + '_account_invoice_' + str(self.id))
#                                                ]],
#                                              {'limit': 1})
#
#        except Exception as e:
#            raise Warning(("Exception when calling remote server $CreateInvoice: %s\n" % e))
#
#        if len(exist) == 0:
#            try:
#                invoice_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'], 'account.invoice', 'create',
#                                                       [{
#                                                           'partner_id': partner_id,
#                                                           'type': self.type,
#                                                           'date_invoice': self.date_invoice,
#                                                       }])
#            except Exception as e:
#                raise Warning(("Exception when calling remote server $RegisterInvoice: %s\n" % e))
#
#            if invoice_id:
#                try:
#                    external_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'], 'ir.model.data',
#                                                            'create', [{
#                            'module': 'ase_replication_server',
#                            'model': 'account.invoice',
#                            'name': str(pc.remote_company_id) + '_account_invoice_' + str(self.id),
#                            'res_id': invoice_id,
#                        }])
#                    return invoice_id
#                except Exception as e:
#                    raise Warning(("Exception when calling remote server $Invoice: %s\n" % e))
#            else:
#                raise Warning(("Error inesperado, por favor inténtelo de nuevo más tarde"))

    @job
    @api.multi
    def send_invoice(self, pc):
        self.ensure_one()
        self._send_invoice_to_remote(pc)

    @api.multi
    def _send_invoice_to_remote(self, pc):

        #for line in self.invoice_line_ids:
        #    line.product_id.is_replicable = True
        #    print(line.product_id.name)
        #    pc.product_ids = [(4, line.product_id.id)]
        #    # Asset Profile of product
        #    line.asset_profile_id.is_replicable = True
        #    pc.account_asset_ids = [(4, line.asset_profile_id.id)]
        #    # Invoice Line Account
        #    line.account_id.is_replicable = True
        #    pc.account_ids = [(4, line.account_id.id)]

        pc.set_parameters(self)

        #conn = pc.setxmlrpc()
        #company_id = pc.set_remote_company(conn)

        #invoice_line_list = self.get_lines(conn, pc)

        #invoice_id = self.write_invoice_to_remote(conn, pc)
        #invoice_line_id = self.write_lines_to_invoice(conn, pc, invoice_line_list)
        #i = 0
        #if invoice_id:
        #    for line in self.invoice_line_ids:
        #        try:
        #            invoice_line_id = conn['models'].execute_kw(pc.db, conn['uid'], conn['rpcp'],
        #                                                        'account.invoice.line', 'create',
        #                                                        [{
        #                                                            'invoice_id': invoice_id,
        #                                                            'product_id': invoice_line_list[i]['product_id'],
        #                                                            'name': line.name,
        #                                                            'account_id': invoice_line_list[i]['account_id'],
        #                                                            'asset_profile_id': invoice_line_list[i]['profile_id'],
        #                                                            'quantity': line.quantity,
        #                                                            'price_unit': line.price_unit,
        #                                                            'discount': line.discount,
        #                                                            'invoice_line_tax_ids': [(6, 0, invoice_line_list[i]['tax_ids'])],
        #                                                            'price_subtotal': line.price_subtotal,
        #                                                        }])
        #            i += 1
        #        except Exception as e:
        #            raise Warning(("Exception when calling remote server $RegisterInvoiceLine: %s\n" % e))


