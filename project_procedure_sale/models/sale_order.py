# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('write_date')
    def create_procedure_tasks_when_confirmed(self):
        for record in self:
            if (record.state == 'sale'):
                for pr in record.project_ids:
                    if (pr.procedure_id.id) and (not pr.task_ids.ids):
                        action = pr.sudo().create_case_tasks()


