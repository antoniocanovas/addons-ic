from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    iset_timesheet_id = fields.Many2one('iset.timesheet')
