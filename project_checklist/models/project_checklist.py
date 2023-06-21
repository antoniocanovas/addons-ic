# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectChecklist(models.Model):
    _name = 'project.checklist'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')

    checklist_ids = fields.One2many('project.checklist.line', 'checklist_id',
                                    string='CheckLists', required=True)


class ProjectChecklistItem(models.Model):
    _name = 'project.checklist.line'
    _description = 'Project Checklist Lines'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    description = fields.Char()
    task_id = fields.Many2one('project.task')
    project_id = fields.Many2one('project.project', related='task_id.project_id', store=True)
    checklist_id = fields.Many2one('project.checklist')
    state = fields.Selection(
        string='Status', required=True, readonly=True, copy=False,
        tracking=True, selection=[
            ('todo', 'To Do'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ], default='todo', )
