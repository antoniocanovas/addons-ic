# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _inherit = 'project.task'

    @api.depends('create_date')
    def _get_contacts_ids(self):
        for record in self:
            contactos = self.env['project.task.contacts'].search([('project_id', '=', record.project_id.id)]).ids
            record['contact_ids'] = [(6, 0, contactos)]

    contact_ids = fields.Many2many('project.task.contacts',compute=_get_contacts_ids,string='Contactos')
