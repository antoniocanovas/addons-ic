# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    roadmap_ids = fields.One2many('project.roadmap', 'task_id', string='Roadmaps', store=True, copy=False)
    roadmap_count = fields.Integer('Roadmaps', compute="_compute_roadmap_count", store=True)
    @api.depends("roadmap_ids.active")
    def _compute_roadmap_count(self):
        for record in self:
            total = 0
            roadmaps = self.env['project.roadmap'].search([('project_id', '=', record.id),('active','in',[True,False])])
            if roadmaps.ids: total = len(roadmaps.ids)
        record['roadmap_count'] = total