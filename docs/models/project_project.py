# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _inherit = 'project.project'

    def _get_docs(self):
        results = self.env['docs.docs'].search([('project_id','=',self.id)])
        self.docs_count = len(results)

    docs_count = fields.Integer('docs',compute=_get_docs,stored=False)

    @api.multi
    def action_view_proyect_docs(self):
        action = self.env.ref(
            'docs.action_task_project_docs').read()[0]
        return action
