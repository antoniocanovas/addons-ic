# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectChecklist(models.Model):
    _name = 'project.checklist'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')

    line_ids = fields.One2many('project.checklist.line', 'checklist_id',
                               string='CheckLists', required=True)
