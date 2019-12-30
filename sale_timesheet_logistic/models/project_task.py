from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    km = fields.Float()
    kg = fields.Float()
    units = fields.Float()
    origin_id = fields.Many2one(
        related='sale_line_id.origin_id',
        string='Collection Point',
        readonly=True,
    )
    delivery_id = fields.Many2one(
        related='sale_line_id.delivery_id',
        string='Delivery Point',
        readonly=True,
    )
    origin_date = fields.Datetime(
        string='Collection Date',
    )
    delivery_date = fields.Datetime(
        string='Delivery Date',
    )

    def delivered_collected(self):
        for task in self:
            if task.origin_date:
                task.delivery_date = fields.datetime.now()
            else:
                task.origin_date = fields.datetime.now()
