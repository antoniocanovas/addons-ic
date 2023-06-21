# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    progress = fields.Float(compute='_compute_progress', string='Progress in %')
    checklist_tmpl_id = fields.Many2one('project.checklist')
    checklist_id = fields.Many2one('project.checklist')
    line_ids = fields.One2many('project.checklist.line', 'task_id',
                                         string='CheckLists', required=True)

    @api.onchange('checklist_tmpl_id')
    def _onchange_checklist_tmpl_id(self):
        if (self.checklist_tmpl_id.id != False) and (self.checklist_id.id == False):
            name = self.checklist_tmpl_id.name
            if self.project_id.name:
                name = self.project_id.name + ": " + name
            new_checklist = self.env['project.checklist'].create({'name': name,
                                                                  'task_id': self.id,
                                                                  'description': self.checklist_tmpl_id.description,
                                                                  })
            self.checklist_id = new_checklist.id

        for li in self.checklist_tmpl_id.checklist_ids:
            new_item = self.env['project.checklist.line'].create({
                'name': li.name,
                'description': li.description,
                'checklist_id': self.checklist_id.id
            })

    @api.onchange('checklist_id')
    def _checklist_move(self):
        for li in self.checklist_id:
            li['task_id'] = self.id

    def _compute_progress(self):
        for rec in self:
            total_completed = 0
            for activity in rec.line_ids:
                if activity.state in ['cancel', 'done', 'in_progress']:
                    total_completed += 1
            if total_completed:
                rec.progress = float(total_completed) / len(
                    rec.line_ids) * 100
            else:
                rec.progress = 0.0
