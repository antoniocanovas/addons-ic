from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class iSetTimesheet(models.Model):
    _name = 'iset.timesheet'
    _description = "TIMESHEET ISET"

    name = fields.Char(string="Name")

    date = fields.Date(string='Date')
    employee_id = fields.Many2one('hr.employee', string="Employee")

    analytic_line_ids = fields.One2many('account.analytic.line', 'iset_timesheet_id', string="Analytic line")

    def calculate_project_time(self):
        time = 0
        for line in self.analytic_line_ids:
            if line.unit_amount:
                time = time + line.unit_amount
        self.project_time = time

    project_time = fields.Float("Project Time", store=False, compute="calculate_project_time")

    repair_fee_ids = fields.One2many('repair.fee', 'iset_timesheet_id', string="Repair fee")
    repair_time = fields.Float("Repair Time")

    mrp_productivity_ids = fields.One2many('mrp.workcenter.productivity', 'iset_timesheet_id', string="MRP")

    def calculate_mrp_time(self):
        time = 0
        for line in self.mrp_productivity_ids:
            if line.duration:
                time = time + line.duration
        self.mrp_time = time

    mrp_time = fields.Float("MRP Time", store=False, compute="calculate_mrp_time")

    def calculate_total_time(self):
        time = 0
        if self.project_time:
            time = time + self.project_time
        if self.mrp_time:
            time = time + self.mrp_time
        self.time = time

    time = fields.Float("Total Time", store=False, compute="calculate_total_time")



