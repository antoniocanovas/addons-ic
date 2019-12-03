# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'


    departamento_id = fields.Many2one('hr.department',string='Departamento')
    linea_expediente_id = fields.Many2one('expediente.tipo.lineas',string='Linea expediente')


