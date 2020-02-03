# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _get_docs(self):
        results = self.env['docs.docs'].search([('task_id', '=', self.id)])
        self.docs_count = len(results)

    docs_count = fields.Integer('Docs', compute=_get_docs,stored=False)

    @api.multi
    def action_view_docs(self):
        action = self.env.ref(
            'docs.action_task_docs').read()[0]
        return action

    def _get_attachments(self):
        results = self.env['ir.attachment'].search([('res_id', '=', self.id)])
        self.attachment_count = len(results)

    attachment_count = fields.Integer('Attachments',compute=_get_attachments,stored=False)

    @api.multi
    def action_view_attachments(self):
        action = self.env.ref(
            'docs.action_task_attachments').read()[0]
        return action
