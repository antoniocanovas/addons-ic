from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    equipment_id = fields.Many2one('maintenance.equipment')

