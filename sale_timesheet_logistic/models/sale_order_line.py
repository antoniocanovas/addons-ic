from odoo import _, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    origin_id = fields.Many2one(
        comodel_name='res.partner',
        string='Collection Point',
    )
    delivery_id = fields.Many2one(
        comodel_name='res.partner',
        string='Delivery Point',
    )
    origin_date = fields.Datetime(
        string='Collection Date',
    )
    delivery_date = fields.Datetime(
        string='Delivery Date',
    )
    product_type = fields.Selection(
        related='product_id.type',
        readonly=True,
    )

    def action_open_task(self):
        return {
            'name': _('Task Data'),
            'view_type': 'tree',
            'view_mode': 'form',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'view_id':
                self.env.ref('sale_timesheet_logistic.view_sale_task_form').id,
            'context': dict(self.env.context),
            'target': 'new',
            'res_id': self.task_id.id,
        }

    def _timesheet_create_task_prepare_values(self, project):
        self.ensure_one()
        values = super()._timesheet_create_task_prepare_values(project)
        if self.origin_date:
            values.update({
                'planned_date_begin': self.origin_date,
                'origin_date': self.origin_date,
            })
        if self.delivery_date:
            values.update({
                'planned_date_end': self.delivery_date,
                'delivery_date': self.delivery_date,
                'date_deadline': self.delivery_date,
            })
        return values
