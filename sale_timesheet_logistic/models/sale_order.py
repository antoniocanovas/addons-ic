from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    profitability = fields.Float(
        compute='_compute_profitability',
    )

    @api.depends('tasks_ids.profitability')
    def _compute_profitability(self):
        for order in self:
            order.profitability = sum(order.mapped('tasks_ids.profitability'))


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
    planned_date_begin = fields.Datetime(
        string='Collection Date',
    )
    planned_date_end = fields.Datetime(
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
        if self.planned_date_begin:
            values.update({
                'planned_date_begin': self.planned_date_begin,
            })
        if self.planned_date_end:
            values.update({
                'planned_date_end': self.planned_date_end,
                'date_deadline': self.planned_date_end,
            })
        return values
