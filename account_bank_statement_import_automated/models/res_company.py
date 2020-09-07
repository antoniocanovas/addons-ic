# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

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
    #journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'bank')])





