from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    quant_ids = fields.One2many('stock.quant', 'employee_id')

    #def _get_equipment_count(self):
    #    results = self.env['maintenance.equipment'].search([('equipment_id', '=', self.id)])
    #    self.equipment_count = len(results)

    #equipment_count = fields.Integer('Credentials', compute=_get_equipment_count, stored=False)

    def action_view_quant(self):
        action = self.env.ref(
            'hr_equipment_stock.action_quant_hr_employee').read()[0]
        return action
