# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectProcedure(models.Model):
    _name = 'project.procedure'
    _description = 'Plantillas de procedimiento de proyectos'

    name = fields.Char(string='Nombre',required=True)
    task_description = fields.Text('Procedimiento')
    store = fields.Boolean(string='Archivado')
    departament_id = fields.Many2one('hr.department',string='Departamento')
    interval = fields.Integer('Días desde inicio exp.')
    user_id = fields.Many2one('res.users',string='usuario')
