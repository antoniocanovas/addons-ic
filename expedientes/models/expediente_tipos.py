# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ExpedienteTipos(models.Model):
    _name = 'expediente.tipos'
    _description = 'Seleccionado en el proyecto de forma requerida si es tipo expediente.'

    name = fields.Char(string='Nombre',required=True)
    linea_ids = fields.One2many('expediente.tipo.lineas','tipo_id',string='Líneas')
    estado = fields.Selection(
        [('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')],default='borrador', string='Estado')
    departamento_id = fields.Many2one('hr.department',string='Departamento',required=True)
    nombre_tarea = fields.Char('Nombre tarea')

