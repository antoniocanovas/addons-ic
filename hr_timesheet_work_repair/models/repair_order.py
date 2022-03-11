from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    def _get_timesheets(self):
        results = self.env['account.analytic.line'].search([('repair_id', '=', self.id)])
        self.timesheets_count = len(results)

    timesheets_count = fields.Integer('Timesheets', compute=_get_timesheets, store=False)
