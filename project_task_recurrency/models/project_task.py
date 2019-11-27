# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'


    rec_type = fields.Selection('Tipo',selection=[('fechabase','En base a la fecha base'),('fechaarchivado','A partir de la fecha de archivado')])
    rec_qty = fields.Integer('Cada')
    rec_date = fields.Date('Fecha base')
    rec_period = fields.Selection('Periodo', selection=[('dias','Días'),('meses','Meses')])
    rec_next_task_id = fields.Many2one('project.task',string='Próx tarea')


