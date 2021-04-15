

from odoo import api, fields, models, _
import paramiko
from os import listdir
import base64
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

STATE = [
    ('draft', 'Draft'),
    ('error', 'Error'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class AccountBankStatementCBI(models.Model):
    _name = 'account.bank.statement.cbi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Importación Automática de Estractos'

    name = fields.Char('Name')
    journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'bank')] )
    state = fields.Selection(
        selection=STATE, string="State", default='draft', track_visibility='onchange'
    )
    bank_statement_attachment_id = fields.Many2one('ir.attachment')
    bank_statement_attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                      relation="m2m_ocr_attachments_rel",
                                      column1="m2m_id",
                                      column2="attachment_id",
                                      string="Bank Statements",
                                      #domain=[('is_bank_statement', '=', True)],
                                    )
    last_connection_date = fields.Datetime(string="Last Connection")

    @api.multi
    def create_sftp_client(self, host, port, username, password, keyfilepath, keyfiletype):
        """
        create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

        Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
        supplied username and supplied password or with the private key in a file with the supplied path.
        If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
        :rtype: SFTPClient object.
        """
        sftp = None
        key = None
        transport = None
        try:
            if keyfilepath is not None:
                # Get private key used to authenticate user.
                if keyfiletype == 'DSA':
                    # The private key is a DSA type key.
                    key = paramiko.DSSKey.from_private_key_file(keyfilepath)
                else:
                    # The private key is a RSA type key.
                    key = paramiko.RSAKey.from_private_key(keyfilepath)

            # Create Transport object using supplied method of authentication.
            transport = paramiko.Transport((host, port))
            transport.connect(None, username, password, key)

            sftp = paramiko.SFTPClient.from_transport(transport)

            return sftp
        except Exception as e:
            print('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
            if sftp is not None:
                sftp.close()
            if transport is not None:
                transport.close()
            pass

    @api.multi
    def get_n43_list(self):
        imported_n43_ids = self.env['account.bank.statement.cbi'].sudo().search([])
        imported_n43_list = []
        for n43 in imported_n43_ids:
            imported_n43_list.append(n43.name)
        return imported_n43_list

    @api.multi
    def move_file_to_downloaded_dir(self, sftpclient, file):
        try:
            sftpclient.rename(file, 'downloaded/%s' % file)  # At this point, you are in remote_path in either case
        except IOError:
            print("ERROR", IOError)

    @api.multi
    def automated_ftp_get_n43_files(self):
        company_id = self.env.user.company_id
        if company_id.ftp_url_cbi and company_id.ftp_port_cbi and company_id.ftp_user_cbi and company_id.ftp_passwd_cbi:
            try:
                sftpclient = self.create_sftp_client(company_id.ftp_url_cbi, company_id.ftp_port_cbi,
                                                     company_id.ftp_user_cbi, company_id.ftp_passwd_cbi, None, 'DSA')
                # List files in the default directory on the remote computer.
                dirlist = sftpclient.listdir('.')

                imported_n43_list = self.get_n43_list()

                for d in dirlist:
                    print('DEBUG', d)
                    path = "/%s" % d
                    result = sftpclient.chdir(path=path)
                    print('Path', path)
                    filelist = sftpclient.listdir('.')
                    print(filelist)

                    for f in filelist:
                        print('DEBUG 2', f)
                        if f != 'Historico':
                            if f not in imported_n43_list:
                                file = sftpclient.file(f, mode='r', bufsize=-1)
                                file_first = file.readline()
                                print("FILE", file_first)
                                bank_number = file_first[12:20]
                                print(bank_number)
                                rename = sftpclient.rename(f,(str(bank_number) + str(f)+ '.n43'))

                                raise ValidationError("HASTA AQUÍ")

                                sftpclient.get(f, '/tmp/%s' % f)
                                try:
                                    bsa_bank_number = f[:24]
                                    raise ValidationError(bsa_bank_number)
                                except Exception as e:
                                    raise ValidationError('Server Error: %s' % e)



                #if 'downloaded' not in dirlist:
                #    try:
                #        sftpclient.mkdir("downloaded")  # Create remote_path
                #    except IOError:
                #        print("ERROR", IOError)

                for row in dirlist:
                    if row != 'Historico':
                        if row not in imported_n43_list:
                            sftpclient.get(row, '/tmp/%s' % row)
                            try:
                                bsa_bank_number = row[:24]
                                raise ValidationError(bsa_bank_number)
                                journal = self.env['account.journal'].sudo().search([])
                                for journal_id in journal:
                                    if journal_id.bank_account_id.acc_number:
                                        bank_account_number = journal_id.bank_account_id.acc_number
                                        bank_account_number = bank_account_number[:29]
                                        bank_account_number = bank_account_number.replace(' ', '')

                                        if bank_account_number == bsa_bank_number:
                                            with open('/tmp/%s' % row, "r+b") as file:
                                                data = file.read()
                                                file.close()
                                                attachment_id = self.env['ir.attachment'].sudo().create({
                                                    'name': row,
                                                    'type': 'binary',
                                                    'datas': base64.b64encode(data),
                                                    'datas_fname': row,
                                                    'store_fname': row,
                                                    'res_model': 'account.bank.statement.cbi',
                                                    # 'res_id': self.id,
                                                    'mimetype': 'text/plain'
                                                })

                                            self.env['account.bank.statement.cbi'].sudo().create({
                                                'name': row,
                                                'journal_id': journal_id.id,
                                                'bank_statement_attachment_id': attachment_id.id,
                                            })
                                            self.move_file_to_downloaded_dir(sftpclient, row)

                            except Exception as e:
                                raise ValidationError('Server Error: %s' % e)
                sftpclient.close()
                time = datetime.now()
                company_id.cbi_last_connection_date = time

            except Exception as e:
                raise ValidationError('Server Error: %s' % e)

        if company_id.cbi_autoimport:
            self.automated_import_files()

    @api.multi
    def import_files(self):
        for record in self:
            if record.state != 'completed':
                if record.journal_id:
                    record = record.with_context(journal_id=record.journal_id.id)

                    bank_statement = record.env['account.bank.statement.import'].create({
                        'data_file': record.bank_statement_attachment_id.datas,
                        'display_name': record.bank_statement_attachment_id.datas_fname,
                        'filename': record.bank_statement_attachment_id.datas_fname,
                    })

                    try:
                        bank_statement.import_file()
                        record.state = 'completed'
                    except Exception as e:
                        record.state = 'error'
                        raise ValidationError('Server Error: %s' % e)

    @api.multi
    def automated_import_files(self):
        imported_n43_ids = self.env['account.bank.statement.cbi'].sudo().search([['state', '=', 'draft']])
        for bsa in imported_n43_ids:

            if bsa.journal_id:
                self = self.with_context(journal_id=bsa.journal_id.id)

                bank_statement = self.env['account.bank.statement.import'].create({
                    'data_file': bsa.bank_statement_attachment_id.datas,
                    'display_name': bsa.bank_statement_attachment_id.datas_fname,
                    'filename': bsa.bank_statement_attachment_id.datas_fname,
                })

                try:
                    bank_statement.import_file()
                    bsa.state = 'completed'
                except Exception as e:
                    bsa.state = 'error'
                    raise ValidationError('Server Error: %s' % e)

