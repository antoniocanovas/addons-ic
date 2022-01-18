from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    work_base_id = fields.Many2one('work.base')
    type_id = fields.Many2one('working.type', 'Type')

