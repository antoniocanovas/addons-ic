from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    work_base_timesheet_id = fields.Many2one('work.base.timesheet')

    #@api.depends('date', 'employee_id', 'create_date','write_date')
    #def update_project_work_base_timesheet(self):
    #    for record in self:
    #        if (record.date) and (record.employee_id.id):
    #            work_base_ts = self.env['work_base.timesheet'].search(
    #                [('date', '=', record.date), ('employee_id', '=', record.employee_id.id)])
    #            if not work_base_ts.id:
    #                name = record.employee_id.name + " - " + str(record.date)
    #                work_base_ts = self.env['work_base.timesheet'].create(
    #                    {'name': name, 'date': record.date, 'employee_id': record.employee_id.id})
    #            record['work_base_timesheet_id'] = work_base_ts.id

    #@api.depends('create_date', 'write_date')
    #def update_project_timesheet(self):
    #    for record in self:
    #        if (record.date) and (record.employee_id.id):
    #            work_base_ts = self.env['work_base.timesheet'].search(
    #                [('date', '=', record.date), ('employee_id', '=', record.employee_id.id)])
    #            if not work_base_ts.id:
    #                name = record.employee_id.name + " - " + str(record.date)
    #                work_base_ts = self.env['work_base.timesheet'].create(
    #                    {'name': name, 'date': record.date, 'employee_id': record.employee_id.id})
    #            record['work_base_timesheet_id'] = work_base_ts.id
