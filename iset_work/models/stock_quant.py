from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    iset_work_id = fields.Many2one('iset.work', related='location_id.iset_work_id')