from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class EquipmentQuantRel(models.Model):
    _name = 'equipment.quant.rel'
    _description = 'Equipment Quant Relational Table'

    quant_id = fields.Many2one('stock.quant')
    equipmnet_id = fields.Many2one('maintenance.equipment')


