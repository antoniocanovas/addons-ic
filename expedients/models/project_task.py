# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'


    departament_id = fields.Many2one('hr.department',string='Departamento')
    expedient_line_id = fields.Many2one('expedient.line.type',string='Linea expediente')


