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


class ProjectChecklist(models.Model):
    _name = 'project.checklist'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')

    checklist_ids = fields.One2many('project.checklist.item', 'checklist_id',
                                    string='CheckList Items', required=True)


class ProjectChecklistItem(models.Model):
    _name = 'project.checklist.item'
    _description = 'Project Checklist Item'

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

    def approve_and_next(self):
        self.state = 'in_progress'

    def mark_completed(self):
        self.state = 'done'

    def mark_canceled(self):
        self.state = 'cancel'

    def reset_stage(self):
        self.state = 'todo'

