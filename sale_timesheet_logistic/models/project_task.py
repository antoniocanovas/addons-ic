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
