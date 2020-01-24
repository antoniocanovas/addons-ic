# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ExpedientTypes(models.Model):
    _name = 'expedient.type'
    _description = 'Types of files.'

    name = fields.Char(string='Nombre',required=True)
    line_ids = fields.One2many('expedient.line.type','type_id',string='Líneas')
    state = fields.Selection(
        [('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')],default='borrador', string='Estado')
    departament_id = fields.Many2one('hr.department',string='Departamento',required=True)
    task_name = fields.Char('Nombre tarea')
    stage_ids = fields.Many2many('project.task.type')

