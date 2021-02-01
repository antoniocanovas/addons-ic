# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    master_db_name = fields.Char(
        string='dbname',
    )

    @api.multi
    def check_instance(self):
        company = self.env.user.company_id

        if not company.master_db_name:
            company.master_db_name = self.env.cr.dbname
        elif company.master_db_name != self.env.cr.dbname:
            fetchmail_servers = self.env['fetchmail.server'].sudo().search([])
            for server in fetchmail_servers:
                server.active = False

            ir_mail_servers = self.env['ir.mail_server'].sudo().search([])
            for ir in ir_mail_servers:
                ir.active = False

