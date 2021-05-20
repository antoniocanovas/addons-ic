from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    iset_timesheet_id = fields.Many2one('iset.timesheet')

    @api.depends('date', 'employee_id', 'create_date','write_date')
    def update_project_iset_timesheet(self):
        for record in self:
            if (record.date) and (record.employee_id.id):
                iset_ts = self.env['iset.timesheet'].search(
                    [('date', '=', record.date), ('employee_id', '=', record.employee_id.id)])
                if not iset_ts.id:
                    name = record.employee_id.name + " - " + str(record.date)
                    iset_ts = self.env['iset.timesheet'].create(
                        {'name': name, 'date': record.date, 'employee_id': record.employee_id.id})
                record['iset_timesheet_id'] = iset_ts.id