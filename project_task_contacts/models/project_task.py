# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _inherit = 'project.task'

    def _get_contacts(self):
        results = self.env['project.task.contacts'].search([('task_id','=',self.id)])
        self.contact_count = len(results)

    contact_count = fields.Integer('Contactos',compute=_get_contacts,stored=False)

    @api.multi
    def action_view_contacts(self):
        action = self.env.ref(
            'project_task_contacts.action_task_contacts').read()[0]
        return action
