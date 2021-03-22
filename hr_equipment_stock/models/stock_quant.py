from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    employee_id = fields.Many2one('hr.employee', related='location_id.employee_id')
    department_id = fields.Many2one('hr.department', related='location_id.department_id')

    @api.onchange('create_date')
    def get_equipment_id(self):
        for record in self:
            equipment = self.env['equipment_quant_rel'].search([('quant_id', '=', record.id)]).equipment_id
            record['equipment_id'] = equipment.id
    equipment_id = fields.Many2one('maintenance.equipment', compute=get_equipment_id, store=False, readonly=True)

