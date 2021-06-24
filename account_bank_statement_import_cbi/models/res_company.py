# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    ftp_user_cbi = fields.Char(
        string='Usuario FTP',
    )
    ftp_url_cbi = fields.Char(
        default='82.223.210.156',
        string='Api Url'
    )
    ftp_port_cbi = fields.Integer(
        default='9122',
        string='Puerto FTP',
    )
    ftp_passwd_cbi = fields.Char(
        string='Password FTP'
    )
    cbi_autoimport = fields.Boolean(
        "Autoimportar",
        help="Si está habilitado tras descargarse la información el extracto será importado automáticamente en el diario del banco correspondiente a la cuenta descargada.",
        default=False,
    )
    cbi_last_connection_date = fields.Datetime(
        'Last connection date'
    )

    @api.multi
    def force_sync_cbi(self):
        if self.ftp_url_cbi and self.ftp_port_cbi and self.ftp_user_cbi and self.ftp_passwd_cbi:
            cbi = self.env['account.bank.statement.cbi'].sudo()
            conn = cbi.automated_ftp_get_n43_files()
            time = datetime.now()
            self.cbi_last_connection_date = time

        else:
            raise ValidationError(
                "You must set ftp server data.")



