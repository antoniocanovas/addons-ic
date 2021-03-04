from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairLine(models.Model):
    _inherit = 'repair.line'

    iset_id = fields.Many2one('isets')