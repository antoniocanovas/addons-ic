# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProjectChecklistLine(models.Model):
    _name = 'project.checklist.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Project Checklist Lines'

    name = fields.Char(required=True)
    active = fields.Boolean('Active', store=True, default=True)
    sequence = fields.Integer(default=1)
    description = fields.Char()
    checklist_id = fields.Many2one('project.checklist')
    task_id = fields.Many2one('project.task', related='checklist_id.task_id')
    project_id = fields.Many2one('project.project', related='task_id.project_id', store=True)
    state = fields.Selection(
        string='Status', required=True, copy=False,
        tracking=True, selection=[
            ('todo', 'To Do'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ], default='todo', )
