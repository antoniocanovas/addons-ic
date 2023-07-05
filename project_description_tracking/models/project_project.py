# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _name = 'project.project'

    description = fields.Char(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    is_template = fields.Boolean('Template')
    line_ids = fields.One2many('project.checklist.line', 'checklist_id',
                               string='CheckLists', required=True)
