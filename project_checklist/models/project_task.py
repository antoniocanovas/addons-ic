# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    progress = fields.Float(compute='_compute_progress', string='Progress in %')
    checklist_tmpl_id = fields.Many2one('project.checklist', store=True, copy=False)
    checklist_id = fields.Many2one('project.checklist', store=True, copy=False)

    @api.depends('checklist_id', 'checklist_id.line_ids')
    def _get_checklist_lines(self):
        self.line_ids = [(6,0,self.checklist_id.line_ids.ids)]
    line_ids = fields.Many2many('project.checklist.line', store=True, compute='_get_checklist_lines')

    @api.onchange('checklist_tmpl_id')
    def _onchange_checklist_tmpl_id(self):
        if (self.checklist_tmpl_id.id != False) and (self.checklist_id.id == False):
            name = self.checklist_tmpl_id.name
            if self.project_id.name:
                name = self.project_id.name + ": " + name
            else:
                name = self.name + ": " + name

            new = self.env['project.checklist'].create({'name': name,
                                                        'project_id': self.project_id.id,
                                                        'description': self.checklist_tmpl_id.description,
                                                        })
            self.checklist_id = new.id

            for li in self.checklist_tmpl_id.line_ids:
                new_item = self.env['project.checklist.line'].create({
                    'name': li.name,
                    'description': li.description,
                    'checklist_id': self.checklist_id.id
                })

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
