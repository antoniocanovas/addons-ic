# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    ftp_user = fields.Char(
        string='Usuario FTP',
    )
    ftp_url = fields.Char(
        default='ftp.tesoralia.com',
        string='Api Url'
    )
    ftp_port = fields.Integer(
        default='22',
        string='Puerto FTP',
    )
    ftp_passwd = fields.Char(
        string='Password FTP'
    )
    last_connection_date = fields.Date(
        'Last connection date'
    )


    @api.multi
    def force_sync_tesoralia(self):
        if self.ftp_url and self.ftp_port and self.ftp_user and self.ftp_passwd:

            tesoralia = self.env['account.bank.statement.tesoralia'].sudo()
            conn = tesoralia.automated_ftp_get_n43_files()

            time = datetime.now()
            self.last_connection_date = time.strftime('%Y-%m-%d %H:%M:%S')

        else:
            raise ValidationError(
                "You must set ftp server data.")



