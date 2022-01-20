from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class WorkBaseTimesheet(models.Model):
    _name = 'work.base.timesheet'
    _description = "TIMESHEET ISET"

    name = fields.Char(string="Name")

    date = fields.Date(string='Date')
    employee_id = fields.Many2one('hr.employee', string="Employee")

    analytic_line_ids = fields.One2many('account.analytic.line', 'work_base_timesheet_id', string="Analytic line")

    def _get_extra_time(self):
        for record in self:
            extra = 0
            for li in record.analytic_line_ids:
                if li.type_id.extra_time == True: extra += li.unit_amount
            for li in record.repair_fee_ids:
                if li.type_id.extra_time == True: extra += li.product_uom_qty
            for li in record.mrp_productivity_ids:
                if li.type_id.extra_time == True: extra += li.duration
            record['extra_time'] = extra

    extra_time = fields.Float(store=False, compute="_get_extra_time")

    def _get_standard_time(self):
        for record in self:
            record.standard_time = record.time - record.extra_time

    standard_time = fields.Float(store=False, compute="_get_standard_time")

    def calculate_project_time(self):
        for record in self:
            time = 0
            for line in record.analytic_line_ids:
                if line.unit_amount:
                    time += line.unit_amount
            record.project_time = time

    project_time = fields.Float("Project Time", store=False, compute="calculate_project_time")

    repair_fee_ids = fields.One2many('repair.fee', 'work_base_timesheet_id', string="Repair fee")

    def calculate_repair_time(self):
        for record in self:
            time = 0
            for line in record.repair_fee_ids:
                if line.product_uom_qty:
                    time += line.product_uom_qty
            record.repair_time = time
    repair_time = fields.Float("Repair Time", store=False, compute="calculate_repair_time")

    mrp_productivity_ids = fields.One2many('mrp.workcenter.productivity', 'work_base_timesheet_id', string="MRP")

    def calculate_mrp_time(self):
        for record in self:
            time = 0
            for line in record.mrp_productivity_ids:
                if line.duration:
                    time += line.duration
            record.mrp_time = time/60

    mrp_time = fields.Float("MRP Time", store=False, compute="calculate_mrp_time")

    def calculate_total_time(self):
        for record in self:
            record.time = record.mrp_time + record.project_time + record.repair_time

    time = fields.Float("Total Time", store=False, compute="calculate_total_time")



