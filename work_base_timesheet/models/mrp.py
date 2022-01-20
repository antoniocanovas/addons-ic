from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    work_base_timesheet_id = fields.Many2one('work.base.timesheet')

    @api.depends('date_end','date_start', 'user_id')
    def update_mrp_work_base_timesheet(self):
        for record in self:
            if (record.date) and (record.employee_id.id):
                work_base_ts = self.env['work.base.timesheet'].search(
                    [('date', '=', record.date), ('employee_id', '=', record.employee_id.id)])
                if not work_base_ts.id:
                    name = record.employee_id.name + " - " + str(record.date)
                    work_base_ts = self.env['work.base.timesheet'].create(
                        {'name': name, 'date': record.date, 'employee_id': record.employee_id.id})
                record['work_base_timesheet_id'] = work_base_ts.id
