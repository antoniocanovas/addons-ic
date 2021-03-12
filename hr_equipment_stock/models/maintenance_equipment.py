from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    quant_ids = fields.One2many('stock.quant', 'equipment_id')

