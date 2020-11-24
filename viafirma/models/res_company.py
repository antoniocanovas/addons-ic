# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'


    last_connection_date = fields.Datetime('Last connection dates')
    #last_conn_date = fields.Datetime('Last connection date')
    user_viafirma = fields.Char('User')
    pass_viafirma = fields.Char('Passwd')
    group_viafirma = fields.Char('Group')

    @api.multi
    def force_sync_viafirma(self):
        viafirmatemplates = self.env['viafirma.templates'].sudo()
        conn = viafirmatemplates.updated_templates()

        time = datetime.now()
        self.last_connection_date = time
