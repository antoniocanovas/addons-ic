# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _name = 'project.task.contacts'
    _description = 'Contactos en tareas'

    partner_id = fields.Many2one('res.partner',string='Contacto')
    task_id = fields.Many2one('project.task',string='Tarea',required=True)
    rol_id = fields.Many2one('res.partner.title',string='rol',required=True)

    @api.depends('task_id')
    def get_tarea(self):
        for record in self:
            if record.task_id.id:
                record['project_id'] = record.task_id.project_id.id

    project_id = fields.Many2one('project.project',compute=get_tarea,string='Proyecto')

