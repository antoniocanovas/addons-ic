# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ExpedienteTramites(models.Model):
    _name = 'expediente.tramites'
    _description = 'Lista de gestiones que pueden tener los expedientes'

    name = fields.Char(string='Nombre',required=True)
    descripcion_tarea = fields.Char('Asunto en tarea')
    archivado = fields.Boolean(string='Archivado')
    departamento_id = fields.Many2one('hr.department',string='Departamento')
    intervalo = fields.Integer('Días desde inicio exp.')
    usuario_id = fields.Many2one('res.users',string='usuario')
