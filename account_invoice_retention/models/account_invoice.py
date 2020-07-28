import base64

from odoo import fields, models, api
import json
import shutil
import requests
from odoo.exceptions import ValidationError
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceRetention(models.Model):
    _inherit = 'account.invoice'

    retention_id = fields.Many2one('account.move', string='Retention', help='Asiento contable para retenciones por garantías de proyecto, el formato es:'
                                                                            '- - - - - - -'
                                                                            '565000 - "cliente" - 1.500 (debe) - 0 (haber)'
                                                                            '430000 - "cliente" - 0 (debe) - 1.000 (haber) - fecha1'
                                                                            '430000 - "cliente" - 0 (debe) - 500 (haber) - fecha2')
    @api.multi
    def _compute_retention_amount(self):
        for record in self:
            total = 0
            if (record.retention_id.id):
                for li in record.retention_id.line_ids:
                    total += li.credit
                record['retention_amount'] = total

    retention_amount = fields.Monetary(string='Total retentions', compute=_compute_retention_amount, store=False)



