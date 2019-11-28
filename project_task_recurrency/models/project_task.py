# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'


    rec_type = fields.Selection(
        [('fechabase','En base a la fecha base'),('fechaarchivado','A partir de la fecha de archivado')]
        ,string='Tipo')
    rec_qty = fields.Integer('Cada')
    rec_date = fields.Date('Fecha base')
    rec_period = fields.Selection(
        [('dias','Días'),('meses','Meses'),('findemes','El último día del mes')]
        ,string='Periodo')
    rec_next_task_id = fields.Many2one('project.task',string='Próx tarea')


