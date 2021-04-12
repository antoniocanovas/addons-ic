from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    iset_work_id = fields.Many2one('iset.work', 'iSet Work')