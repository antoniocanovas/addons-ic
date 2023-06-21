# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: LINTO C T(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    progress = fields.Float(compute='_compute_progress', string='Progress in %')
    checklist_tmpl_id = fields.Many2one('project.checklist')
    checklist_id = fields.Many2one('project.checklist')
    checklist_item_ids = fields.One2many('project.checklist.item', 'task_id',
                                         string='CheckList Items', required=True)

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
            new_item = self.env['project.checklist.item'].create({
                'name': li.name,
                'description': li.description,
                'checklist_id': self.checklist_id.id
            })

    @api.onchange('checklist_id')
    def _onchange_project_id(self):
        self.checklist_item_ids = []
        checklist = self.env['project.checklist'].search(
            [('name', '=', self.checklist_id.name)])
        for rec in checklist:
            self.checklist_item_ids += rec.checklist_ids

    def _compute_progress(self):
        for rec in self:
            total_completed = 0
            for activity in rec.checklist_item_ids:
                if activity.state in ['cancel', 'done', 'in_progress']:
                    total_completed += 1
            if total_completed:
                rec.progress = float(total_completed) / len(
                    rec.checklist_item_ids) * 100
            else:
                rec.progress = 0.0
