from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairFee(models.Model):
    _inherit = 'repair.fee'

    iset_timesheet_id = fields.Many2one('iset.timesheet')
