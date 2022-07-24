# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('status')
    def create_tasks_if_procedure_when_sold(self):
        if (self.state == 'sale'):
            for pr in self.project_ids:
                if (pr.procedure_id.id) and (not pr.task_ids.ids):
                    action = pr.sudo().create_case_tasks()


