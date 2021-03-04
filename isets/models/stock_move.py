from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    iset_id = fields.Many2one('isets')