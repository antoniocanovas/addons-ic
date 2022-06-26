# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    roadmap_ids = fields.One2many('project.roadmap', 'task_id', string='Roadmaps', store=True, copy=False)
