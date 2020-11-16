# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    ftp_user_tesoralia = fields.Char(
        string='Usuario FTP',
    )
    ftp_url_tesoralia = fields.Char(
        default='ftp.tesoralia.com',
        string='Api Url'
    )
    ftp_port_tesoralia = fields.Integer(
        default='22',
        string='Puerto FTP',
    )
    ftp_passwd_tesoralia = fields.Char(
        string='Password FTP'
    )
    tesoralia_autoimport = fields.Boolean(
        "Autoimportar",
        help="Si está habilitado tras descargarse la información el extracto será importado automáticamente en el diario del banco correspondiente a la cuenta descargada.",
        default=False,
    )
    tesoralia_last_connection_date = fields.Datetime(
        'Last connection date'
    )


    @api.multi
    def force_sync_tesoralia(self):
        if self.ftp_url_tesoralia and self.ftp_port_tesoralia and self.ftp_user_tesoralia and self.ftp_passwd_tesoralia:

            tesoralia = self.env['account.bank.statement.tesoralia'].sudo()
            conn = tesoralia.automated_ftp_get_n43_files()

            time = datetime.now()
            self.tesoralia_last_connection_date = time

        else:
            raise ValidationError(
                "You must set ftp server data.")



