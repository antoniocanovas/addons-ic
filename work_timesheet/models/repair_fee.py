from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class RepairFee(models.Model):
    _inherit = 'repair.fee'

    work_timesheet_id = fields.Many2one('work.timesheet')

    @api.depends('date', 'employee_id')
    def update_repair_work_timesheet(self):
        for record in self:
            if (record.date) and (record.employee_id.id):
                work_ts = self.env['work.timesheet'].search(
                    [('date', '=', record.date), ('employee_id', '=', record.employee_id.id)])
                if not work_ts.id:
                    name = record.employee_id.name + " - " + str(record.date)
                    work_ts = self.env['work.timesheet'].create(
                        {'name': name, 'date': record.date, 'employee_id': record.employee_id.id})
                record['work_timesheet_id'] = work_ts.id
