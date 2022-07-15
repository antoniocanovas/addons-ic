# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

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


class ConfigClient(models.Model):
    _inherit = 'partner.credentials'

    client_api_key = fields.Char(
        string='Ocr Key',
    )

    def get_line_objects(self, invoice):
        product_list = []
        for line in invoice.invoice_line_ids:
            if line.product_id:
                line.product_id.is_replicable = True
                self.product_p_ids = [(4, line.product_id.id)]
            # Asset Profile of product
            if line.asset_profile_id:
                line.asset_profile_id.is_replicable = True
                self.account_asset_ids = [(4, line.asset_profile_id.id)]
            # Invoice Line Account
            if line.account_id:
                line.account_id.is_replicable = True
                self.account_ids = [(4, line.account_id.id)]

        return True

    def get_lines(self, conn, invoice):
        invoice_line_list = []
        line_dic = {}
        for line in invoice.invoice_line_ids:
            if line.product_id:
                product_id = self.get_product(line.product_id, conn)
            else:
                product_id = False
            if line.account_id:
                account_id = self.get_account(line.account_id, conn)
            if line.asset_profile_id:
                profile_id = self.get_asset_profile(line.asset_profile_id, conn)
            else:
                profile_id = False
            if line.tax_ids:
                tax_ids = self.get_taxes(line.tax_ids, conn)
            else:
                tax_ids = []

            line_dic = {
                'product_id': product_id,
                'account_id': account_id,
                'profile_id': profile_id,
                'tax_ids': tax_ids,
            }
            invoice_line_list.append(line_dic)
        return invoice_line_list

    def check_partner_in_remote(self, partner, conn, invoice):
        partner_exist = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                  'res.partner', 'search_read',
                                                  [[('vat', '=', partner.vat)]],
                                                  {'fields': ['id'], 'limit': 1})
        if not partner_exist:
            try:
                partner_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'res.partner', 'create',
                                                       [{
                                                           'name': partner.name,
                                                           'vat': partner.vat,
                                                           'company_type': 'company'

                                                       }])

                return partner_id
            except Exception as e:
                invoice.invoice_sync_error = ("Error comprobando proveedor: %s\n" % invoice.ref)
                invoice.remote_state = 'error'
                raise Warning(("Exception when calling remote server $CreatePartner: %s\n" % e))
        return partner_exist[0]['id']

    ##### FOR V12 ################
    def write_invoice_to_remote_v12(self, conn, invoice):
        partner_id = self.check_partner_in_remote(invoice.partner_id, conn, invoice)

        try:
            invoice_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                   'account.invoice', 'search',
                                                   [[('reference', '=', invoice.ref),
                                                     ('partner_id', '=', partner_id),
                                                     ]],
                                                   {'limit': 1})
        except Exception as e:
            raise Warning(("Exception when calling remote server $CreateInvoice: %s\n" % e))

        if invoice_id:
            invoice.invoice_sync_error = ("La factura ya existe en el cliente: %s\n" % invoice.ref)
            invoice.remote_state = 'sent'
            return False
        else:
            if invoice.remote_type:
                type_for_remote = invoice.remote_type
            else:
                type_for_remote = invoice.type
            try:
                invoice_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'account.invoice', 'create',
                                                       [{
                                                           'reference': invoice.ref,
                                                           'partner_id': partner_id,
                                                           'type': type_for_remote,
                                                           'date_invoice': invoice.invoice_date,
                                                           #'date_due': invoice.date_due,
                                                       }])
                invoice.remote_state = 'sent'
            except Exception as e:
                invoice.invoice_sync_error = ("Error al crear la factura: %s\n" % invoice.ref)
                invoice.remote_state = 'error'
                raise Warning(("Exception when calling remote server $RegisterInvoice: %s\n" % e))

            if invoice_id:
                return invoice_id
            else:
                invoice.remote_state = 'sent'
                return False

    def write_invoice_to_remote(self, conn, invoice):
        partner_id = self.check_partner_in_remote(invoice.partner_id, conn, invoice)
        try:
            invoice_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                              'account.move', 'search',
                                              [[('ref', '=', invoice.ref),
                                                ('partner_id', '=', partner_id),
                                                ]],
                                              {'limit': 1})
        except Exception as e:
            raise Warning(("Exception when calling remote server $CreateInvoice: %s\n" % e))

        if invoice_id:
            invoice.invoice_sync_error = ("La factura ya existe en el cliente: %s\n" % invoice.ref)
            invoice.remote_state = 'sent'
            return False
        else:
            if invoice.remote_type:
                type_for_remote = invoice.remote_type
            else:
                type_for_remote = invoice.move_type
            try:
                invoice_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'account.move', 'create',
                                                       [{
                                                           'ref': invoice.ref,
                                                           'partner_id': partner_id,
                                                           'move_type': type_for_remote,
                                                           'invoice_date': invoice.invoice_date,
                                                           #'invoice_payment_term_id': invoice.invoice_payment_term_id,
                                                       }])
                invoice.remote_state = 'sent'
            except Exception as e:
                invoice.invoice_sync_error = ("Error al crear la factura: %s\n" % invoice.ref)
                invoice.remote_state = 'error'
                raise Warning(("Exception when calling remote server $RegisterInvoice: %s\n" % e))

            if invoice_id:
                return invoice_id
            else:
                invoice.remote_state = 'sent'
                return False

    def create_invoice_lines_v12(self, conn, invoice_id, invoice, invoice_line_list):
        i = 0
        for line in invoice.invoice_line_ids:
            try:
                invoice_line_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                            'account.invoice.line', 'create',
                                                            [{
                                                                'invoice_id': invoice_id,
                                                                'product_id': invoice_line_list[i]['product_id'],
                                                                'name': line.name,
                                                                'account_id': invoice_line_list[i]['account_id'],
                                                                'asset_profile_id': invoice_line_list[i]['profile_id'],
                                                                'quantity': line.quantity,
                                                                'price_unit': line.price_unit,
                                                                'discount': line.discount,
                                                                'invoice_line_tax_ids': [
                                                                    (6, 0, invoice_line_list[i]['tax_ids'])],
                                                                'price_subtotal': line.price_subtotal,
                                                            }])
                i += 1
            except Exception as e:
                invoice.invoice_sync_error = ("Error creando líneas de factura: %s\n" % invoice.ref)
                invoice.remote_state = 'error'
                raise Warning(("Exception when calling remote server $RegisterInvoiceLine: %s\n" % e))
        if invoice_line_id:
            return invoice_line_id
        else:
            invoice.invoice_sync_error = ("Error creando líneas de factura: %s\n" % invoice.ref)
            invoice.remote_state = 'error'
            return False

    def create_invoice_lines(self, conn, invoice_id, invoice, invoice_line_list):
        i = 0
        invoice_lines = []
        partner_id = self.check_partner_in_remote(invoice.partner_id, conn, invoice)
        for line in invoice.invoice_line_ids:
            invoice_lines.append((0, 0, {
                'product_id':invoice_line_list[i]['product_id'],
                'name': line.name,
                'account_id':invoice_line_list[i]['account_id'],
                'partner_id':partner_id,
                'price_unit':line.price_unit,
                'tax_ids': [(6, 0, invoice_line_list[i]['tax_ids'])],
            }))
            invoice_lines.append((0, 0, {
                'name':line.name or '/',
                'account_id':invoice_line_list[i]['account_id'],
                'partner_id':partner_id,
                'exclude_from_invoice_tab':True}))
            i += 1

            try:
                invoice_line_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                            'account.move', 'write', [[invoice_id], {
                        'invoice_line_ids': invoice_lines,
                    }])

                #invoice_line_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                #                                            'account.move.line', 'create',
                #                                            [{
                #                                                'invoice_id': invoice_id,
                #                                                'product_id': invoice_line_list[i]['product_id'],
                #                                                'name': line.name,
                #                                                'account_id': invoice_line_list[i]['account_id'],
                #                                                'asset_profile_id': invoice_line_list[i]['profile_id'],
                #                                                'quantity': line.quantity,
                #                                                'price_unit': line.price_unit,
                #                                                'discount': line.discount,
                #                                                'tax_ids': [
                #                                                    (6, 0, invoice_line_list[i]['tax_ids'])],
                #                                                'price_subtotal': line.price_subtotal,
                #                                            }])

            except Exception as e:
                invoice.invoice_sync_error = ("Error creando líneas de factura: %s\n" % invoice.ref)
                invoice.remote_state = 'error'
                raise Warning(("Exception when calling remote server $RegisterInvoiceLine: %s\n" % e))
        if invoice_line_id:
            return invoice_line_id
        else:
            return False

    def compute_invoice_v12(self, invoice, invoice_id, conn):
        invoice.remote_state = 'sent'
        invoice.remote_send_failed = False
        try:
            compute_tax = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                    'account.invoice', 'compute_taxes',
                                                    [[invoice_id], ])
        except Exception as e:
            raise Warning((" Error On tax calc : %s\n" % e))
        try:
            compute_tax = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                    'account.invoice', 'action_invoice_open',
                                                    [[invoice_id], ])
        except Exception as e:
            invoice.invoice_sync_error = ("Error validando factura: %s\n" % invoice.ref)
            invoice.remote_state = 'error'
            raise Warning((" Error Validating remote invoice : %s\n" % e))

    def compute_invoice(self, invoice, invoice_id, conn):
        invoice.remote_state = 'sent'
        invoice.remote_send_failed = False
        try:
            compute_tax = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                    'account.move', 'compute_taxes',
                                                    [[invoice_id], ])
        except Exception as e:
            raise Warning((" Error On tax calc : %s\n" % e))
        try:
            compute_tax = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'],
                                                    'account.move', 'action_invoice_open',
                                                    [[invoice_id], ])
        except Exception as e:
            invoice.invoice_sync_error = ("Error validando factura: %s\n" % invoice.ref)
            invoice.remote_state = 'error'
            raise Warning((" Error Validating remote invoice : %s\n" % e))

    def create_attachment_v12(self, conn, invoice, invoice_id):

        try:
            invoice_attachment = self.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'account.move'),
                ('res_id', '=', invoice.id)
            ])

            attachment_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'ir.attachment', 'create',
                                                      [{
                                                          'name': invoice_attachment.name,
                                                          'type': 'binary',
                                                          'datas': invoice_attachment.datas,
                                                          'display_name': invoice_attachment.display_name,
                                                          'store_fname': invoice_attachment.store_fname,
                                                          'res_model': 'account.invoice',
                                                          'res_id': invoice_id,
                                                          'mimetype': invoice_attachment.mimetype
                                                      }])

            return attachment_id
        except Exception as e:
            invoice.remote_state = 'error'
            invoice.invoice_sync_error = ("No se ha podido crear el adjunto"
                                          " en servidor remoto: %s\n" % e)

    def create_attachment(self, conn, invoice, invoice_id):

        try:
            invoice_attachment = self.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'account.move'),
                ('res_id', '=', invoice.id)
            ])

            attachment_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'ir.attachment', 'create',
                                                      [{
                                                          'name': invoice_attachment.name,
                                                          'type': 'binary',
                                                          'datas': invoice_attachment.datas,
                                                          'display_name': invoice_attachment.display_name,
                                                          'store_fname': invoice_attachment.store_fname,
                                                          'res_model': 'account.move',
                                                          'res_id': invoice_id,
                                                          'mimetype': invoice_attachment.mimetype
                                                      }])
            return attachment_id
        except Exception as e:
            invoice.remote_state = 'error'
            invoice.invoice_sync_error = ("No se ha podido crear el adjunto"
                                          " en servidor remoto: %s\n" % e)

    def create_message_post_v12(self, conn, invoice_id, attachment_id):
        try:
            message_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'mail.message',
                                                   'create',
                                                   [{
                                                       'res_id': invoice_id,
                                                       'model': 'account.invoice',
                                                       'body': 'Documentos',
                                                       'attachment_ids': [(6, 0, [attachment_id])],
                                                   }])
            return message_id
        except Exception as e:
            raise Warning(("Exception when calling remote server $Message_post: %s\n" % e))

    def create_message_post(self, conn, invoice_id, attachment_id):
        try:
            message_id = conn['models'].execute_kw(self.db, conn['uid'], conn['rpcp'], 'mail.message',
                                                   'create',
                                                   [{
                                                       'res_id': invoice_id,
                                                       'model': 'account.move',
                                                       'body': 'Documentos',
                                                       'attachment_ids': [(6, 0, [attachment_id])],
                                                   }])
            return message_id
        except Exception as e:
            raise Warning(("Exception when calling remote server $Message_post: %s\n" % e))

    def que_set_parameters(self):
        # new_delay = self.sudo().with_delay().set_parameters()
        for pc in self:
            company = self.env.user.company_id
            # Set ETA
            jobs = self.env['queue.job'].sudo().search(["|",
                                                        ('state', '=', 'pending'), ('state', '=', 'enqueued')
                                                        ])
            eta = 20 + (len(jobs) * 20)

            if not self.db or not self.url:
                raise Warning((
                    "Revise los campos 'Base de datos' y 'Servidor' en la pestaña SSO"
                ))
            elif not self.remote_company_id or self.remote_company_id == "0":
                raise Warning((
                    "Debe especificar el ID de la empresa en la pestaña SSO"
                ))
            else:
                queue_obj = self.env['queue.job'].sudo()
                new_delay = pc.sudo().with_context(
                    company_id=company.id
                ).with_delay(eta=eta).set_parameters(False)
                job = queue_obj.search([
                    ('uuid', '=', new_delay.uuid)
                ], limit=1)
                pc.sudo().ase_replication_jobs_ids |= job

    def set_parameters(self, invoice):
        conn = self.setxmlrpc()
        self.set_remote_company(conn)

        if invoice:
            objects = self.get_line_objects(invoice)

        self.check_dependences()

        # Replicate
        if len(self.account_ids) > 0:
            for account in self.account_ids:
                acc_id = self.get_account(account, conn)
                if not acc_id:
                    self.write_account(account, conn)
                    self.last_change = datetime.now()
        if len(self.product_p_ids) > 0:
            for product in self.product_p_ids:
                prod_id = self.get_product(product, conn)
                if not prod_id:
                    self.write_products(product, conn)
                    self.last_change = datetime.now()

        if len(self.asset_group_ids) > 0:
            for asset_group in self.asset_group_ids:
                group_id = self.get_asset_groups(asset_group, conn)
                if not group_id:
                    self.write_asset_group(asset_group, conn)
                    self.last_change = datetime.now()

        if len(self.account_asset_ids) > 0:
            for account_asset in self.account_asset_ids:
                profile_id = self.get_asset_profile(account_asset, conn)
                if not profile_id:
                    self.write_asset_profile(account_asset, conn)
                    self.last_change = datetime.now()

        # set parent for groups
        if len(self.asset_group_ids) > 0:
            for asset_group in self.asset_group_ids:
                self.write_asset_group_parent(asset_group, conn)

        # Set asset Profile for accounts
        if len(self.account_ids) > 0:
            for account in self.account_ids:
                self.write_asset_profile_account(account, conn)

        if invoice:

            if conn['version'] == '14.0':
                invoice_line_list = self.get_lines(conn, invoice)
                if invoice_line_list:
                    invoice_id = self.write_invoice_to_remote(conn, invoice)
                    if invoice_id:
                        invoice_line_id = self.create_invoice_lines(conn, invoice_id, invoice, invoice_line_list)
                        if invoice_line_id:
                            #self.compute_invoice(invoice, invoice_id, conn)
                            attachment_id = self.create_attachment(conn, invoice, invoice_id)
                            if attachment_id:
                                message_id = self.create_message_post(conn, invoice_id, attachment_id)
                        else:
                            invoice.remote_send_failed = True
            else:
                invoice_line_list = self.get_lines(conn, invoice)
                if invoice_line_list:
                    invoice_id = self.write_invoice_to_remote_v12(conn, invoice)
                    if invoice_id:
                        invoice_line_id = self.create_invoice_lines_v12(conn, invoice_id, invoice, invoice_line_list)
                        if invoice_line_id:
                            self.compute_invoice_v12(invoice, invoice_id, conn)
                            attachment_id = self.create_attachment_v12(conn, invoice, invoice_id)
                            if attachment_id:
                                message_id = self.create_message_post_v12(conn, invoice_id, attachment_id)
                        else:
                            invoice.remote_send_failed = True


